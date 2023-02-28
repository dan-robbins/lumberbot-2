from discord.ext import commands

class cannon_cog(commands.Cog):
    def __init__(self, bot: commands.Bot, owner_id):
        self.bot = bot
        self.owner_id = owner_id

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.bot.get_user(int(self.owner_id)).send("Member {}/{} left {}!".format(member.name, member.nick, member.guild.name))

        #TODO add cannon sound