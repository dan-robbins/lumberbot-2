import asyncio
import discord
import random
from discord.ext import commands

class cannon_cog(commands.Cog):
    def __init__(self, bot: commands.Bot, owner_id: int):
        self.bot = bot
        self.owner_id = owner_id

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        await self.bot.get_user(self.owner_id).send("Member {}#{}/{} left {}!".format(member.name, member.discriminator, member.nick if member.nick is not None else member.name, member.guild.name))
        voice_client = discord.utils.get(self.bot.voice_clients, guild=member.guild)
        if not (voice_client and voice_client.is_connected()):
            max_users = 0
            max_channel = None
            for channel in member.guild.voice_channels:
                num_users = len(channel.members)
                if num_users > max_users:
                    max_users = num_users
                    max_channel = channel
            if max_users > 0:
                voice_client = await max_channel.connect()
            else:
                voice_client = None
        if voice_client is not None:
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(random.choice(["sounds/cannon2.mp3", "sounds/cannon3.mp3", "sounds/cannon4.mp3", "sounds/cannon5.mp3"])))
            discord.opus.load_opus("libopus.so.0")
            voice_client.play(source)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.id == self.bot.user.id:
            return

        elif before.channel is None:
            voice = after.channel.guild.voice_client
            time = 0
            while True:
                await asyncio.sleep(1)
                time = time + 1
                if voice.is_playing() and not voice.is_paused():
                    time = 0
                if time == 60:
                    await voice.disconnect()
                if not voice.is_connected():
                    break

    @commands.command(name='disconnect')
    async def _disconnect(self, ctx: commands.Context):
        """Disconnects from the current voice channel."""

        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if not (voice_client and voice_client.is_connected()):
            await ctx.channel.send("Not connected to a voice channel")
            return
        else:
            await voice_client.disconnect()
