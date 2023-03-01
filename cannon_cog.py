import asyncio
import discord
from discord.ext import commands

class cannon_cog(commands.Cog):
    def __init__(self, bot: commands.Bot, owner_id: int):
        self.bot = bot
        self.owner_id = owner_id

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.bot.get_user(self.owner_id).send("Member {}/{} left {}!".format(member.name, member.nick, member.guild.name))
        max_users = 0
        max_channel = None
        for channel in member.guild.voice_channels:
            num_users = len(channel.members)
            if num_users > max_users:
                max_users = num_users
                max_channel = channel
        
        voice_client = await max_channel.connect()
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("sounds/cannon3.mp3"))
        voice_client.play(source)
        while voice_client.is_playing():
            await asyncio.sleep(1)
        
        await voice_client.disconnect()