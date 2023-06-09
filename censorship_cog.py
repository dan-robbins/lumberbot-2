import re
import discord
from discord.ext import commands

class censorship_cog(commands.Cog):
    def __init__(self, bot: commands.Bot, owner_id: int):
        self.bot = bot
        self.owner_id = owner_id
        self.regex1 = re.compile(r"(?:(?:f(?: o r e s k i |\.o\.r\.e\.s\.k\.i\.|oresk[1i])|4sk[1i])n|beforeskin|(?:fo(?:re? |ure)|phore)skin|forskine|(?:fo(?:rce|urs)|phors)kin)")
        self.regex2 = re.compile(r"(?:circum(?:ci[sz](?:i(?:ng|on)|ed?)|si[sz](?:i(?:ng|on)|ed?)|ci)|ircum(?:ci[sz](?:i(?:ng|on)|ed?)|si[sz](?:i(?:ng|on)|ed?)|ci))")
        self.regex3 = re.compile(r"(?:(?:(?:force|(?:for[kr]|4)s)|fours)|pfors)kin")
        self.regex4 = re.compile(r"p* *h* *f* *h* *o+ *r* *c* *e* *s+ *k+ *i+ *n+")
        self.regex5 = re.compile(r"fo(?:r(?:e(?:, S|\-s)|ced)|urs )kin")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user or message.author.bot:
            return
        
        if self.regex1.search(message.content.lower()) is not None or self.regex2.search(message.content.lower()) is not None or self.regex3.search(message.content.lower()) is not None or self.regex4.search(message.content.lower()) is not None:
            await message.delete()
            await message.author.send("Your message \"{}\" was removed. This incident will be recorded and reported to the shadow council.".format(message.content))
            await self.bot.get_user(self.owner_id).send("Deleted message \"{}\" from {} in {}".format(message.content, message.author.name, message.channel.guild.name))