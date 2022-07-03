from email import message
import discord
from discord.ext import commands, pages
from numpy import True_
from pycoingecko import CoinGeckoAPI
from discord.commands import slash_command, Option
from utils.DatabaseHelper import DatabaseHelper
from datetime import timedelta, datetime
#TO DO: 
#Change how the bots messages look
#Most of these should be in discord.Embed
class Chat(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=[922988296878063686], name='timeout', description='Times out the user provided.')
    async def timeout(self, ctx, member: Option(discord.Member, description='The member you want to timeout', required = True), 
    reason: Option(str, description='Must be at least 5 characters long', required=True),
    days: Option(int, required=False),
    hours: Option(int, required=False),
    minutes: Option(int, required=False)):
        if len(reason) < 5:
            await ctx.respond("Kick reason must be 5 or more characters in length.")
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
        #https://docs.pycord.dev/en/master/api.html#embed
        embed = discord.Embed(
            #__ underline the text
            title = "__Action: Timeout__",
            colour = discord.Colour.green(),
            timestamp = datetime.utcnow()
        )

        embed.set_image(url = member.display_avatar.url)
        embed.set_thumbnail(url = member.display_avatar.url)
        embed.add_field(name='Reason: ', value = reason, inline=False)
        embed.add_field(name='Duration', value = f"Days: {days}, Hours: {hours}, Minutes: {minutes}", inline=False)
        embed.add_field(name='User', value = member.mention, inline=False)

        try:
            await member.timeout(until=datetime.utcnow() + duration, reason=reason)
            #await ctx.respond(f"<@{member.id}> has been muted for {days} days, {hours} hours, and {minutes} minutes.\n<@{ctx.author.id}> has carried out this action for reason: {reason}")
            await ctx.respond(embed=embed)
        
        except discord.HTTPException as e:
            await ctx.respond(f"Error while timing out user: {member.name}")
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
        #defer is required if response will take longer than 3 seconds
        #it shouldn't take 3 seconds to query database, but it is here just in case
        await ctx.defer()
        helper = DatabaseHelper()
        result = helper.query_users_history(str(ctx.guild.id), str(user.id))
        if result is None:
            await ctx.respond(f"User: {user.id} has no messages in this server!")
        else:
            #the start of the list contains the oldest messages, therefore start at the end for newest
            message_pages = []
            for message_data in result[::-1]:
                #creating an embed and adding it to it's own page
                message_pages.append(self.create_chat_embed(user, message_data))

            paginator = pages.Paginator(pages=message_pages)
            await paginator.respond(ctx.interaction, ephemeral=False)
    
    @slash_command(guild_ids=[922988296878063686], name='users_deleted_messages', description='Returns the users deleted messages.')
    async def users_deleted_messages(self, ctx, user: Option(discord.Member, description='The users who deleted messages you want to query.', required = True)):
        await ctx.defer()
        helper = DatabaseHelper()
        result = helper.query_deleted_messages(str(ctx.guild.id), str(user.id))
        if result == "nodeletedmessages":
            await ctx.respond(f"No deleted messages found for: {user.mention}")
        else: 
            #the start of the list contains the oldest messages, therefore start at the end for newest
            message_pages = []
            for message_data in result[::-1]:
                #creating an embed and adding it to it's own page
                message_pages.append(self.create_deleted_embed(user, message_data))

            paginator = pages.Paginator(pages=message_pages)
            await paginator.respond(ctx.interaction, ephemeral=False)

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
    
    def create_chat_embed(self, user, message_contents):
        #message_conents: "SELECT msg, message_id, edited_or_not, edited_time, published_time, deleted_or_not"
        #message_conents is a tuple by default
        message_contents = list(message_contents)
        #Transforming 0 and 1 ints to boolean to display on the embed
        if (int(message_contents[2]) == 0):
            message_contents[2] = 'False'
        else: message_contents[2] = 'True'

        if (int(message_contents[5]) == 0):
            message_contents[5] = 'False'
        else: message_contents[5] = 'True'

        embed = discord.Embed(
            #__ to underline the text
            title = "__Chat History__",
            colour = discord.Colour.green(),
        )

        embed.set_thumbnail(url = user.display_avatar.url)
        embed.add_field(name='User: ', value = user.name, inline=False)
        embed.add_field(name='Message_id: ', value=message_contents[1], inline=False)
        embed.add_field(name='Edited Flag: ', value=message_contents[2], inline=False)
        if (message_contents == 'True'):
            sliced_time = message_contents[3][11:19]
            embed.add_field(name='Edited Time: ', value=sliced_time, inline=False)    
        embed.add_field(name='Deleted Flag: ', value=message_contents[5], inline=False)
        embed.add_field(name='Published Time: ', value=message_contents[4][11:19], inline=False)
        embed.add_field(name='Message: ', value=message_contents[0], inline=False)
        return embed

    def create_deleted_embed(self, user, message_contents):
        #SELECT msg, message_id, published_time, deleted_or_not
        #message_conents is a tuple by default
        message_contents = list(message_contents)
        #Transforming 0 and 1 ints to boolean to display on the embed
        if (int(message_contents[3]) == 0):
            message_contents[3] = 'False'
        else: message_contents[3] = 'True'

        embed = discord.Embed(
            #__ to underline the text
            title = "__Deleted Chat History__",
            colour = discord.Colour.green(),
        )

        embed.set_thumbnail(url = user.display_avatar.url)
        embed.add_field(name='User: ', value = user.name, inline=False)
        embed.add_field(name='Message_id: ', value=message_contents[1], inline=False)   
        embed.add_field(name='Deleted Flag: ', value=message_contents[3], inline=False)
        embed.add_field(name='Published Time: ', value=message_contents[2][11:19], inline=False)
        embed.add_field(name='Message: ', value=message_contents[0], inline=False)
        return embed

def setup(bot):
    bot.add_cog(Chat(bot))