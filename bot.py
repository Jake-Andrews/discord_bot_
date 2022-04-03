from discord.ext import commands
import discord
import os
from pycoingecko import CoinGeckoAPI
from discord.commands import Option
from dotenv import load_dotenv

#To do  
#Clean up the project (file managemnt, etc...)  - Somewhat done
#Properly document everything
#Add roles
#Stalk command
#Fix on_message_edit 
#Add proper logging to the project
#Add cogs
#Add a database file that will connect and disconnect
#stalk_channel_history which will give the user a history for the past x minutes of the server
#And will include all of the edits that have been made, includes photos, embeds, etc....
#Add a twitch live feature, possibly cozy.tv
#Consider something for docker
#Mess around with adding support for twitter/reddit

load_dotenv()
bot = commands.Bot(command_prefix='.')
cg = CoinGeckoAPI()
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

cogs_list = []

for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and filename != '__init__.py':
        cogs_list.append("cogs." + filename[:-3])

for cog in cogs_list:
    try:
        bot.load_extension(cog)
    except Exception as e: 
        print(f"Error loading cog file: {e}")

try:   
    bot.run(DISCORD_TOKEN)

except Exception as e: 
    print(f"Error {e} when trying to log in")