import discord
from discord.ext import commands
import asyncio
import re

def parse_time(timestr: str) -> int:
    """
    Parse a time string like "60s", "5m", "2h" into seconds.
    Returns an integer (seconds).
    """
    match = re.fullmatch(r"(\d+)([smh])", timestr.lower())
    if not match:
        raise ValueError("Invalid time format. Use formats like 60s, 5m, 2h.")
    
    value, unit = match.groups()
    value = int(value)
    
    if unit == "s":
        return value
    elif unit == "m":
        return value * 60
    elif unit == "h":
        return value * 3600
    else:
        raise ValueError("Invalid time unit.")

def format_time(seconds: int) -> str:
    """
    Format seconds into H:M:S or M:S as appropriate.
    """
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h > 0:
        return f"{h}h {m}m {s}s"
    elif m > 0:
        return f"{m}m {s}s"
    else:
        return f"{s}s"

class timer_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # channel_id: list of {"task", "message", "stop_event", "user", "end_time"}
        self.active_timers = {}

    @commands.command(name="timer")
    async def start_timer(self, ctx, user: discord.Member = None, duration: str = None):
        """
        Start a timer that pings the mentioned user after <duration>.
        Usage: +timer @user 5m
        """
        if user is None or duration is None:
            await ctx.send("Usage: `+timer @user <time>` (e.g., 60s, 5m, 2h)")
            return

        try:
            time_seconds = parse_time(duration)
        except ValueError as e:
            await ctx.send(str(e))
            return

        # Send initial message
        timer_msg = await ctx.send(
            f"⏳ Timer started for {user.mention}, will ping in **{duration}**.\n"
            f"React with 🛑 or use `+timer_stop` to cancel."
        )

        try:
            await timer_msg.add_reaction("🛑")
        except discord.Forbidden:
            pass  # Bot may not have permission

        stop_event = asyncio.Event()
        end_time = asyncio.get_event_loop().time() + time_seconds

        async def timer_task():
            try:
                await asyncio.wait_for(stop_event.wait(), timeout=time_seconds)
                if stop_event.is_set():
                    await ctx.send(f"🛑 Timer for {user.mention} was stopped early.")
                else:
                    await ctx.send(f"⏰ Time’s up! {user.mention}")
            except asyncio.TimeoutError:
                await ctx.send(f"⏰ Time’s up! {user.mention}")
            finally:
                # Remove this timer from the channel's list
                self.active_timers[ctx.channel.id].remove(timer_data)
                if not self.active_timers[ctx.channel.id]:
                    del self.active_timers[ctx.channel.id]

        # Store the timer
        timer_data = {
            "task": None,
            "message": timer_msg,
            "stop_event": stop_event,
            "user": user,
            "end_time": end_time,
        }
        timer_task_obj = asyncio.create_task(timer_task())
        timer_data["task"] = timer_task_obj

        self.active_timers.setdefault(ctx.channel.id, []).append(timer_data)

    @commands.command(name="timer_stop")
    async def stop_timer(self, ctx, index: int = None):
        """
        Stop a timer in this channel.
        - No index: stops the most recent timer.
        - With index: stops that specific timer (from +timers list).
        """
        if ctx.channel.id not in self.active_timers or not self.active_timers[ctx.channel.id]:
            await ctx.send("No active timers in this channel.")
            return

        timers = self.active_timers[ctx.channel.id]

        if index is None:
            # Stop the most recent timer
            timer_data = timers[-1]
        else:
            if index < 1 or index > len(timers):
                await ctx.send(f"Invalid index. Use `+timers` to see valid indexes (1–{len(timers)}).")
                return
            timer_data = timers[index - 1]

        timer_data["stop_event"].set()
        await ctx.send(f"🛑 Timer for {timer_data['user'].mention} stop requested.")

    @commands.command(name="timers")
    async def list_timers(self, ctx):
        """
        List all active timers in this channel with remaining time.
        """
        if ctx.channel.id not in self.active_timers or not self.active_timers[ctx.channel.id]:
            await ctx.send("No active timers in this channel.")
            return

        now = asyncio.get_event_loop().time()
        lines = []
        for i, timer_data in enumerate(self.active_timers[ctx.channel.id], start=1):
            remaining = max(0, int(timer_data["end_time"] - now))
            lines.append(f"{i}. {timer_data['user'].mention} → {format_time(remaining)} left")

        msg = "\n".join(lines)
        await ctx.send(f"⏳ Active timers:\n{msg}")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """
        Stop the timer if someone reacts with 🛑
        """
        if user.bot:
            return
        if str(reaction.emoji) == "🛑":
            for channel_id, timers in list(self.active_timers.items()):
                for timer_data in list(timers):
                    if reaction.message.id == timer_data["message"].id:
                        timer_data["stop_event"].set()
                        await reaction.message.channel.send(
                            f"🛑 Timer for {timer_data['user'].mention} canceled via reaction."
                        )
                        return  # Only cancel one timer
