import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

from wood_cog import wood_cog
from livecounter_cog import livecounter_cog
from cannon_cog import cannon_cog
from censorship_cog import censorship_cog
from touchdown_cog import touchdown_cog
from waluigi_cog import waluigi_cog
from eval_cog import eval_cog
from ping_cog import ping_cog
from dm_cog import dm_cog

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
WOOD_ID = int(os.getenv('WOOD_ID'))
WOOD_EMOJI = int(os.getenv('WOOD_EMOJI'))
OWNER_ID = int(os.getenv('OWNER_ID'))
NEAL_ID = int(os.getenv('NEAL_ID'))
intents = discord.Intents.all()
prefix = '+'

async def add_cogs(bot: commands.Bot):
    await bot.add_cog(wood_cog(bot, wood_id=WOOD_ID, wood_posts=True, wood_emoji=WOOD_EMOJI))
    await bot.add_cog(livecounter_cog(bot))
    await bot.add_cog(cannon_cog(bot, owner_id=OWNER_ID))
    await bot.add_cog(censorship_cog(bot, owner_id=OWNER_ID))
    await bot.add_cog(touchdown_cog(bot))
    await bot.add_cog(waluigi_cog(bot, neal_id=NEAL_ID))
    await bot.add_cog(eval_cog(bot, owner_id=OWNER_ID))
    await bot.add_cog(ping_cog(bot))
    await bot.add_cog(dm_cog(bot, owner_id=OWNER_ID))

bot = commands.Bot(command_prefix=prefix, description='Lumberbot v2', intents=intents)

@bot.event
async def on_ready():
    await add_cogs(bot)
    print('Logged in as:\n{0.user.name}\n{0.user.id}'.format(bot))

bot.run(TOKEN)