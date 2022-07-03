from discord.ext import commands
import discord
import os
from pycoingecko import CoinGeckoAPI
from discord.commands import Option
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
intents = discord.Intents.all()
bot = commands.Bot(intents=intents)
cg = CoinGeckoAPI()

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
        print(str(cog))
    except Exception as e: 
        print(f"Error loading cog file: {e}")

try:   
    bot.run(DISCORD_TOKEN)
except Exception as e: 
    print(f"Error {e} when trying to log in")