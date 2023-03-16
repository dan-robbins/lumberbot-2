import json
import discord
from discord.ext import commands

class touchdown_cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user or message.author.bot:
            return

        if message.content == 'touchdowns' or message.content == 'score' or message.content == 'scoreboard':
            with open('touchdowns.json', 'r') as openfile:
                touchdowns = json.load(openfile)
            touchdowns = dict(sorted(touchdowns.items(), key=lambda item: item[1], reverse=True))
            val = "Touchdowns:\n"
            for x in touchdowns:
                name = str(x)
                val = val + "{}: {}\n".format(name[0].upper() + name[1:], touchdowns[x]) 
            val = val[:-1]
            await message.channel.send(val)
            return

    @commands.command(name='touchdown')
    async def _touchdown(self, ctx: commands.Context, arg1: str, arg2: str):
        """Add a touchdown for the specified name.

        Usage: touchdown <name> to add a touchdown for <name>
        touchdown remove <name> to remove a touchdown from <name>
        """

        if arg1 == None or len(arg1) == 0:
            return
        
        if arg1 == "remove":
            if arg2 == None or len(arg2) == 0:
                return
            with open('touchdowns.json', 'r') as openfile:
                touchdowns = json.load(openfile)
            if arg2.lower() in touchdowns:
                touchdowns[arg2.lower()] = int(touchdowns[arg2.lower()])-1
                with open("touchdowns.json", "w") as outfile:
                    json.dump(touchdowns, outfile)
                await ctx.channel.send("Touchdown removed for {}.".format(arg2[0].upper() + arg2[1:].lower()))
        else:
            val = 0
            with open('touchdowns.json', 'r') as openfile:
                touchdowns = json.load(openfile)
            if arg1.lower() in touchdowns:
                val = int(touchdowns[arg1.lower()])
            touchdowns[arg1.lower()] = val + 1
            with open("touchdowns.json", "w") as outfile:
                json.dump(touchdowns, outfile)
            await ctx.channel.send("Touchdown {}!".format(arg1[0].upper() + arg1[1:].lower()))

    @commands.command(name='touchdowns', aliases=['score', 'scoreboard'])
    async def _touchdowns(self, ctx: commands.Context):
        """Print the current touchdown scoreboard.
        """
        
        with open('touchdowns.json', 'r') as openfile:
            touchdowns = json.load(openfile)
        touchdowns = dict(sorted(touchdowns.items(), key=lambda item: item[1], reverse=True))
        val = "Touchdowns:\n"
        for x in touchdowns:
            name = str(x)
            val = val + "{}: {}\n".format(name[0].upper() + name[1:], touchdowns[x]) 
        val = val[:-1]
        await ctx.message.channel.send(val)
        return