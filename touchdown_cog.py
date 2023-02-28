import json
from discord.ext import commands

class touchdown_cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
            return

        if message.content == 'touchdowns' or message.content == 'score' or message.content == 'scoreboard':
            with open('touchdowns.json', 'r') as openfile:
                touchdowns = json.load(openfile)
            val = "Touchdowns:\n"
            for x in touchdowns:
                name = str(x)
                val = val + "{}: {}\n".format(name[0].upper() + name[1:], touchdowns[x]) 
            val = val[:-1]
            await message.channel.send(val)

    @commands.command(name='touchdown')
    async def _touchdown(self, ctx: commands.Context, arg: str):
        """Add a touchdown for the specified name.

        Usage: touchdown <name> to add a touchdown for <name>
        touchdown remove <name> to remove a touchdown from <name>
        """

        if len(arg) == 0:
            return
        args = arg.split()
        if len(args) == 0:
            return
        if len(args[0]) == 0:
            return
        
        if args[0] == "remove":
            if len(args) == 1:
                return
            if len(args[1]) == 0:
                return
            with open('touchdowns.json', 'r') as openfile:
                touchdowns = json.load(openfile)
            if args[1].lower() in touchdowns:
                touchdowns[args[1].lower()] = int(touchdowns[args[1].lower()])-1
                with open("touchdowns.json", "w") as outfile:
                    json.dump(touchdowns, outfile)
                await ctx.channel.send("Touchdown removed for {}.".format(args[1][0].upper() + args[1][1:].lower()))
        else:
            val = 0
            with open('touchdowns.json', 'r') as openfile:
                touchdowns = json.load(openfile)
            if args[0].lower() in touchdowns:
                val = int(touchdowns[args[0].lower()])
            touchdowns[args[0].lower()] = val + 1
            with open("touchdowns.json", "w") as outfile:
                json.dump(touchdowns, outfile)
            await ctx.channel.send("Touchdown {}!".format(args[0][0].upper() + args[0][1:].lower()))