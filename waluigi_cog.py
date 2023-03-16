from discord.ext import commands
import random

class waluigi_cog(commands.Cog):
    def __init__(self, bot: commands.Bot, neal_id: int):
        self.bot = bot
        self.neal_id = neal_id
        self.responses = [
            "https://i.imgur.com/NM9dE18.jpg",
            "http://i.imgur.com/jAPpdaE.jpg",
            "https://i.imgur.com/1dTZOx9.jpg",
            "https://i.imgur.com/gANV354.png",
            "https://i.imgur.com/G80NvVs.jpg",
            "https://i.imgur.com/snDLShN.png",
            "https://i.imgur.com/SpEhovO.jpg",
            "https://i.imgur.com/rnodf7X.jpg",
            "https://i.imgur.com/VoN41wR.png",
            "https://i.imgur.com/6eERewD.jpg",
            "https://i.imgur.com/mHMqUnu.jpg",
            "https://i.imgur.com/r50XVDd.jpg",
            "https://i.imgur.com/8noTA67.png",
            "https://i.imgur.com/k0THQ4s.jpg",
            "https://i.imgur.com/OTGWbqF.jpg",
            "https://i.imgur.com/xZ3jAUA.jpg",
            "https://i.imgur.com/o2HUg9x.jpg",
            "https://i.imgur.com/MDtAvmK.jpg",
            "https://i.imgur.com/HqghE19.jpg",
            "https://i.imgur.com/69AgXiB.png",
            "https://i.imgur.com/HmeqCMK.jpg",
            "https://i.imgur.com/cPe3Zpt.png",
            "http://i.imgur.com/qeCpN41.jpg",
            "https://i.imgur.com/uVCiT7T.jpg",
            "https://i.imgur.com/mwIbees.jpg",
            "https://i.imgur.com/5AV5k9t.png",
            "https://i.imgur.com/JoZgHaG.jpg",
            "https://i.imgur.com/UD6EIqc.png",
            "https://i.imgur.com/bVP45QL.jpg",
            "https://i.imgur.com/n0WSEmm.jpg",
            "https://i.imgur.com/wj8b3TJ.jpg",
            "https://i.imgur.com/uIvEObB.png",
            "https://i.imgur.com/t9pcdaf.jpg",
            "https://i.imgur.com/ELhsMyI.jpg",
            "https://i.imgur.com/24F5Po6.jpg",
            "https://i.imgur.com/MGLThP4.jpg",
            "https://i.imgur.com/u2Y1vOO.jpg",
            "https://i.imgur.com/zerUjsT.jpg",
            "https://i.imgur.com/od4Of0e.png",
            "https://i.imgur.com/PwG4GXn.jpg",
            "https://i.imgur.com/EcMASZB.jpg",
            "https://i.imgur.com/4DRxmtE.jpg",
            "https://i.imgur.com/0DBSdLI.jpg",
            "https://i.imgur.com/3fI7oyo.jpg",
            "https://i.imgur.com/pjzFy1g.png",
            "https://i.imgur.com/myngWSM.jpg",
            "https://i.imgur.com/hU8TbqZ.png",
            "https://www.youtube.com/watch?v=m9I4xuArxhA",
            "https://www.youtube.com/watch?v=Rf9PClQKOmg",
            "https://www.youtube.com/watch?v=yQ0iTDafXuM",
            "https://www.youtube.com/watch?v=cg2ZWibCwKE"
        ]

    @commands.command(name='waluigi')
    async def _waluigi(self, ctx: commands.Context):
        """Waluigi in smash???
        """

        response = random.choice(self.responses)
        await ctx.channel.send("{} {}".format(ctx.channel.guild.get_member(self.neal_id).mention, response))