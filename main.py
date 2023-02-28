import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

from music_cog import music_cog
from wood_cog import wood_cog
from livecounter_cog import livecounter_cog

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
WOOD_ID = os.getenv('WOOD_ID')
intents = discord.Intents.all()

async def add_cogs(bot: commands.Bot):
    await bot.add_cog(music_cog(bot))
    #await bot.add_cog(wood_cog(bot, wood_id=WOOD_ID, wood_posts=True, blocked=False))
    #await bot.add_cog(livecounter_cog(bot))

bot = commands.Bot(command_prefix='music.', description='Yet another music bot.', intents=intents)

@bot.event
async def on_ready():
    await add_cogs(bot)
    print('Logged in as:\n{0.user.name}\n{0.user.id}'.format(bot))

bot.run(TOKEN)