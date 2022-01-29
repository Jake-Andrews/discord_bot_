import discord
from discord.ext import commands
from pycoingecko import CoinGeckoAPI
from discord.commands import slash_command, Option
from utils.DatabaseHelper import DatabaseHelper


class Chat(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.message_command(guild_ids=[922988296878063686], name='editedmessage')
    async def editedmessage(self, ctx, msg : discord.Message):
        await ctx.defer()
        helper = DatabaseHelper()
        result = helper.query_edited_messages(str(ctx.guild.id), str(msg.id))
        if result == "noedit":
            await ctx.respond("This message has not been edited!")
        else: await ctx.respond(result)

    #Format this differently, maybe use embeds?
    @slash_command(guild_ids=[922988296878063686], name='chat', description='Returns the users chat history.')
    async def chat(self, ctx, user: Option(discord.Member, description='The user whos chat history you want.', required = True)):
        await ctx.defer()
        helper = DatabaseHelper()
        result = helper.query_users_history(str(ctx.guild.id), str(user.id))
        if result is None:
            ctx.respond(f"User: {user.id} has no messages in this server!")
        
        await ctx.respond(f"The users history contains: {result}.\nThe user has: {len(result)} messages total.")

    @commands.Cog.listener("on_message_edit")  
    async def on_message_edit(self, before, after):
        helper = DatabaseHelper()
        helper.insert_message_edit(str(before.author.id), str(before.id), str(before.guild.id), after.edited_at, after.content)

    @commands.Cog.listener("on_message") 
    async def on_message(self, message):
        print(f"Content: {message.content}")
        helper = DatabaseHelper()
        helper.insert_message(message.content, str(message.id), str(message.channel), str(message.author.id), str(message.created_at), str(message.guild.id))

    @commands.Cog.listener("on_guild_join")
    async def on_guild_join(self, guild):
        helper = DatabaseHelper()
        helper.insert_guild(str(guild.id))

def setup(bot):
    bot.add_cog(Chat(bot))