import json
import discord
from discord.ext import commands

class wood_cog(commands.Cog):
    def __init__(self, bot: commands.Bot, wood_id: int, wood_posts: bool, blocked: bool, wood_emoji: int):
        self.bot = bot
        self.WOOD_ID = wood_id
        self.wood_posts = wood_posts
        self.wood_emoji = bot.get_emoji(wood_emoji)
        self.blocked = blocked

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        if type(reaction.emoji) is not str and reaction.emoji.id == self.wood_emoji.id and (reaction.message.author.id == self.WOOD_ID or reaction.message.author == self.bot.user):
            with open('records.json', 'r') as openfile:
                records = json.load(openfile)
            records["woods"] = int(records["woods"]) + 1
            if int(records["woods"]) % 500 == 0:
                await reaction.message.channel.send("Milestone reached! {} total woods!".format(records["woods"]))
            if reaction.count > int(records["record"]):
                await reaction.message.channel.send("New record! {} woods on a single post! Previous record was {} woods.".format(reaction.count, records["record"]))
                records["record"] = reaction.count
            with open("records.json", "w") as outfile:
                json.dump(records, outfile)
        elif type(reaction.emoji) is not str and reaction.emoji.id == self.wood_emoji.id and not (reaction.message.author.id == self.WOOD_ID or reaction.message.author == self.bot.user) and user.id == self.WOOD_ID:
            reaction.remove(user)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.User):
        if type(reaction.emoji) is not str and reaction.emoji.id == self.wood_emoji.id and (reaction.message.author.id == self.WOOD_ID or reaction.message.author == self.bot.user):
            with open('records.json', 'r') as openfile:
                records = json.load(openfile)
            records["woods"] = int(records["woods"]) - 1
            with open("records.json", "w") as outfile:
                json.dump(records, outfile)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user or message.author.bot:
            return
        
        if self.wood_posts and message.author.id == self.WOOD_ID and not self.blocked:
            await message.add_reaction(self.wood_emoji)

        if self.wood_posts and message.author.id == self.WOOD_ID and self.blocked:
            m = await message.channel.send("{} All hail the king! {}".format(self.wood_emoji, self.wood_emoji))
            await m.add_reaction(self.wood_emoji)