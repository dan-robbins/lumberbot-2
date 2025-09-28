import discord
from discord.ext import commands, tasks
from astropy.time import Time
from astropy.coordinates import moon_phase_angle
import astropy.units as u
import datetime
import pytz
import numpy as np

class moon_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1382437039076544574  # target text channel
        self.prev_illum = None
        self.last_state = {}  # Track in/out of monitored phases
        self.monitored_phases = ["Waxing Gibbous"]  # <-- configurable list
        self.check_moon_phase.start()

    def cog_unload(self):
        self.check_moon_phase.cancel()

    def get_moon_illumination(self, time):
        """Return fractional illumination (0 = new, 1 = full)."""
        phase_angle = moon_phase_angle(time)
        illum = (1 + np.cos(phase_angle.radian)) / 2
        return illum

    def is_waxing(self, current, previous):
        """Return True if waxing (illumination increasing)."""
        if previous is None:
            return None
        return current > previous

    def classify_phase(self, illum, waxing):
        """
        Classify moon phase more precisely.
        Returns string name.
        """
        if waxing is None:
            return "Unknown"

        if illum < 0.03:
            return "New Moon"
        elif illum < 0.5 and waxing:
            return "Waxing Crescent"
        elif abs(illum - 0.5) < 0.02 and waxing:
            return "First Quarter"
        elif illum >= 0.5 and illum < 1.0 and waxing:
            return "Waxing Gibbous"
        elif illum > 0.97:
            return "Full Moon"
        elif illum >= 0.5 and not waxing:
            return "Waning Gibbous"
        elif abs(illum - 0.5) < 0.02 and not waxing:
            return "Last Quarter"
        else:
            return "Waning Crescent"

    @tasks.loop(hours=1)
    async def check_moon_phase(self):
        """
        Background task (non-blocking).
        Checks every hour if the moon enters/exits monitored phases.
        """
        # New York local time
        tz = pytz.timezone("America/New_York")
        now = datetime.datetime.now(tz)

        # Convert to Astropy time
        t = Time(now)

        # Illumination fraction
        illum = self.get_moon_illumination(t)
        waxing = self.is_waxing(illum, self.prev_illum)

        # Classify
        phase = self.classify_phase(illum, waxing)

        # Check against monitored phases
        for monitored in self.monitored_phases:
            in_phase = (phase == monitored)
            last = self.last_state.get(monitored, None)

            if last is not None and in_phase != last:
                channel = self.bot.get_channel(self.channel_id)
                if channel:
                    if in_phase:
                        await channel.send(
                            f"🌙 The Moon has **ENTERED** the {monitored} phase! "
                            f"(Illumination: {illum:.1%})"
                        )
                    else:
                        await channel.send(
                            f"🌙 The Moon has **EXITED** the {monitored} phase! "
                            f"(Illumination: {illum:.1%})"
                        )

            # Update state
            self.last_state[monitored] = in_phase

        self.prev_illum = illum

    @check_moon_phase.before_loop
    async def before_check(self):
        await self.bot.wait_until_ready()

    @commands.command(name="moon")
    async def moon_command(self, ctx):
        """
        Responds with the current moon phase and illumination.
        """
        tz = pytz.timezone("America/New_York")
        now = datetime.datetime.now(tz)
        t = Time(now)

        illum = self.get_moon_illumination(t)
        waxing = None if self.prev_illum is None else self.is_waxing(illum, self.prev_illum)
        phase = self.classify_phase(illum, waxing)

        await ctx.send(
            f"🌙 Current Moon Phase: **{phase}** "
            f"(Illumination: {illum:.1%}) — {now.strftime('%Y-%m-%d %H:%M %Z')}"
        )
