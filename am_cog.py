import discord
from discord.ext import commands, tasks
import pytz
from datetime import datetime, timedelta

AUDIO_FILE = "sounds/3am.mp3"

class ThreeAMCog(commands.Cog):
    def __init__(self, bot: commands.Bot, am_guild_id: int):
        self.bot = bot
        self.am_guild_id = am_guild_id
        self.daily_task.start()

    def cog_unload(self):
        self.daily_task.cancel()

    @tasks.loop(hours=24)
    async def daily_task(self):
        """Runs once a day at 3:00 AM New York time."""
        tz = pytz.timezone("America/New_York")
        now = datetime.now(tz)

        # If we've already passed 3 AM today, schedule for tomorrow
        target_time = tz.localize(datetime(now.year, now.month, now.day, 3, 0, 0))
        if now >= target_time:
            target_time += timedelta(days=1)

        print(f"[3AM COG] Sleeping until next 3 AM at {target_time.isoformat()}")
        await discord.utils.sleep_until(target_time)

        print("[3AM COG] It's 3 AM! Attempting to play audio...")
        await self.play_audio()

    @daily_task.before_loop
    async def before_daily_task(self):
        await self.bot.wait_until_ready()
        print("[3AM COG] Daily task loop started and waiting until first run...")

    async def play_audio(self):
        guild = self.bot.get_guild(self.am_guild_id)
        if guild is None:
            print(f"[3AM COG] Guild with ID {self.am_guild_id} not found.")
            return

        # Find the most populated voice channel with at least 1 member
        populated_channels = [
            channel for channel in guild.voice_channels if len(channel.members) > 0
        ]
        if not populated_channels:
            print("[3AM COG] No populated voice channels found at 3 AM. Doing nothing.")
            return

        most_populated = max(populated_channels, key=lambda c: len(c.members))
        print(f"[3AM COG] Most populated channel: {most_populated.name} "
              f"with {len(most_populated.members)} member(s).")

        # Connect and play
        try:
            vc = await most_populated.connect()
            print(f"[3AM COG] Connected to {most_populated.name}.")
        except discord.ClientException:
            print("[3AM COG] Already connected to a voice channel. Skipping.")
            return

        if not vc.is_playing():
            def after_playing(error):
                if error:
                    print(f"[3AM COG] Error while playing audio: {error}")
                else:
                    print("[3AM COG] Finished playing audio. Disconnecting...")
                fut = vc.disconnect()
                self.bot.loop.create_task(fut)

            print(f"[3AM COG] Now playing {AUDIO_FILE}...")
            vc.play(discord.FFmpegPCMAudio(AUDIO_FILE), after=after_playing)