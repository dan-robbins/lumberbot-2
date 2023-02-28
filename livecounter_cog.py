import json
from discord.ext import commands

class livecounter_cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.content == 'livecounter':
            with open('records.json', 'r') as openfile:
                records = json.load(openfile)
            await message.channel.send("A total of {} woods since January 18th 2018, with a record of {} woods on a single post. A total of {} Danny ace{}.".format(records["woods"], records["record"], records["aces"], '' if int(records["aces"]) == 1 else 's'))
