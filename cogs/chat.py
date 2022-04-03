import discord
from discord.ext import commands
from pycoingecko import CoinGeckoAPI
from discord.commands import slash_command, Option
from utils.DatabaseHelper import DatabaseHelper
from datetime import timedelta, datetime
#TO DO: 
#Change how the bots messages look
#Most of these should be in discord.Embed
#Add commands to check if certain twitch/youtubers are live
#Some sort of 60 second loop for this 
#The admin of the server or mod should be able to add twitch and youtube channels 
#Store them in a text file
class Chat(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=[922988296878063686], name='timeout', description='Times out the user provided.')
    async def timeout(self, ctx, member: Option(discord.Member, description='The member you want to timeout', required = True), 
    reason: Option(str, description='Must be at least 5 characters long'),
    days: Option(int, required=False),
    hours: Option(int, required=False),
    minutes: Option(int, required=False)):
        if member.id == ctx.author.id:
            await ctx.respond("You cannot timeout yourself!")
        if member.id == self.bot.user.id:
            await ctx.respond("You cannot timeout me!")
        
        #https://docs.pycord.dev/en/master/api.html#discord.Permissions.moderate_members
        if member.guild_permissions.moderate_members:
            await ctx.respond("You cannot timeout a moderator!")
        
        if days is None:
            days = 0
        if hours is None:
            hours = 0
        if minutes is None:
            minutes = 0

        print(f"Days: {days}, Hours: {hours}, Minutes: {minutes}")
        duration = timedelta(days = days, hours = hours, minutes = minutes)
        embed = discord.Embed(
            title = "Action: Timeout",
            description = f'User ID: {member.id}',
            colour = discord.Colour.red()
        )

        embed.set_image(url = member.display_avatar.url)
        #embed.set_thumbnail(url = member.display_avatar.url)
        #embed.set_author(name = member.display_name, url = member.mention)
        embed.add_field(name='Duration', value = f"Days: {days}, Hours: {hours}, Minutes: {minutes}", inline=False)
        embed.add_field(name='User', value = member.mention, inline=False)

        try:
            await member.timeout(until=datetime.utcnow() + duration, reason=reason)
            #await ctx.respond(f"<@{member.id}> has been muted for {days} days, {hours} hours, and {minutes} minutes.\n<@{ctx.author.id}> has carried out this action for reason: {reason}")
            await ctx.respond(embed=embed)
        
        except discord.HTTPException as e:
            print("Http exception: {e}")

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
    
    @slash_command(guild_ids=[922988296878063686], name='users_deleted_messages', description='Returns the users deleted messages.')
    async def users_deleted_messages(self, ctx, user: Option(discord.Member, description='The users who deleted messages you want to query.', required = True)):
        await ctx.defer()
        helper = DatabaseHelper()
        result = helper.query_deleted_messages(str(ctx.guild.id), str(user.id))
        if result == "nodeletedmessages":
            await ctx.respond(f"No deleted messages found for: {user.mention}")
        else: await ctx.respond(f"The user: {user.mention}'s history contains these deleted messages: \n{result}")

    @commands.Cog.listener("on_message_edit")  
    async def on_message_edit(self, before, after):
        if before.author.id == self.bot.user.id:
            return
        helper = DatabaseHelper()
        helper.insert_message_edit(before, after)

    @commands.Cog.listener("on_message") 
    async def on_message(self, message):
        if message.author.id == self.bot.user.id:
            return
        print(f"Content: {message.content}")
        helper = DatabaseHelper()
        helper.insert_message(message.content, str(message.id), str(message.channel), str(message.author.id), str(message.created_at), str(message.guild.id))
        #Think of a way to do a long list of these
        #Send the message to a function which searches a list in a random order and sends a message 
        #With the first match
        word = self.check_contents(message)
        if word:    
            await message.channel.send(word)

    @commands.Cog.listener("on_guild_join")
    async def on_guild_join(self, guild):
        helper = DatabaseHelper()
        helper.insert_guild(str(guild.id))

    @commands.Cog.listener("on_message_delete")
    async def on_message_delete(self, message):
        helper = DatabaseHelper()
        helper.update_deleted_message(message)

    def check_contents(self, message):
        target_words = ["Based on what?", "Who is joe?", ""]
        for i, word in enumerate(target_words):
            if word in message.content.lower(): 
                break
        return target_words[i]

def setup(bot):
    bot.add_cog(Chat(bot))