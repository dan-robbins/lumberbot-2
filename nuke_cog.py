import asyncio
import discord
import random
from discord.ext import commands

class nuke_cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="nuke")
    async def nuke_command(self, ctx):
        myGuild = await self.bot.fetch_guild(382437037314932756)
        voice_client = discord.utils.get(self.bot.voice_clients, guild=myGuild)
        if not (voice_client and voice_client.is_connected()):
            max_users = 0
            max_channel = None
            for channel in myGuild.voice_channels:
                num_users = len(channel.members)
                if num_users > max_users:
                    max_users = num_users
                    max_channel = channel
            if max_users > 0:
                voice_client = await max_channel.connect()
            else:
                voice_client = None
        if voice_client is not None:
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("sounds/tactical-nuke.mp3"))
            discord.opus.load_opus("libopus.so.0")
            voice_client.play(source)

