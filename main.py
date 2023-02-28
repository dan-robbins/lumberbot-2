import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

from music_cog import music_cog
from wood_cog import wood_cog
from livecounter_cog import livecounter_cog
from cannon_cog import cannon_cog

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
WOOD_ID = os.getenv('WOOD_ID')
WOOD_EMOJI = os.getenv('WOOD_EMOJI')
OWNER_ID = os.getenv('OWNER_ID')
intents = discord.Intents.all()
prefix = 'music.'

async def add_cogs(bot: commands.Bot):
    await bot.add_cog(music_cog(bot))
    #await bot.add_cog(wood_cog(bot, wood_id=WOOD_ID, wood_posts=True, blocked=False, wood_emoji=WOOD_EMOJI))
    #await bot.add_cog(livecounter_cog(bot))
    #await bot.add_cog(cannon_cog(bot, owner_id=OWNER_ID))

bot = commands.Bot(command_prefix=prefix, description='Yet another music bot.', intents=intents)

@bot.event
async def on_ready():
    await add_cogs(bot)
    print('Logged in as:\n{0.user.name}\n{0.user.id}'.format(bot))

bot.run(TOKEN)