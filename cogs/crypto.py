import discord
from discord.ext import commands
from pycoingecko import CoinGeckoAPI
from discord.commands import slash_command
from discord.commands import Option

class Crypto(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.cg = CoinGeckoAPI()
        self.coinList = [
        'Bitcoin',
        'Ethereum',
        'Litecoin',
        'Dogecoin',
        'Bitcoin Cash',
        ]
        self.fiatList = [
            'USD',
            'EUR',
            'GBP',
            'JPY',
            'CAD',
            'AUD'
        ]

    def getPrice(self, cryptoId, fiatId):
        return self.cg.get_price(ids=cryptoId, vs_currencies=fiatId)


    def displayCoinList(self):
        str = ''
        for coin in self.coinList:
            str += f'{coin}\n'
        
        return str

    def displayFiatList(self):
        str = ''
        for fiat in self.fiatList:
            str += f'{fiat}\n'
        
        return str

    def parsePriceJson(self, priceJson, fiat):
        str = ''
            
        for coin in priceJson:
            str += '{} -> '.format(coin.capitalize())
            for fiat in priceJson[coin]:
                str += '\n\t\t{} {:,.2f}'.format(fiat, priceJson[coin][fiat])
            str += '\n\n'
        
        return str 

    def getCommandList(self):
        return """
        /help -> Returns a list of avaliable commands. 
        /cryptoList -> Returns a list of the support cryptocurrencies.
        /fiatList -> Returns a list of avaliable Fiat.
        /getPrice (crypto) (fiat) -> Returns: The current price of the cryptocurrency in the given Fiat.
        """

    @slash_command(guild_ids=[922988296878063686], name='fiatlist', description='Returns a list of supported fiat.')
    async def fiatlist(self, ctx):
        await ctx.respond(self.displayFiatList())

    @slash_command(guild_ids=[922988296878063686], name='help', description='Returns a list of commands.')
    async def help(self, ctx):
        await ctx.respond(self.getCommandList())

    @slash_command(guild_ids=[922988296878063686], name='getprice', description='Takes a cryptocurrency (required) and a fiat (default = USD)')
    async def getprice(self, ctx,    
        crypto: Option(str, 'Cryptocurrency', required=False, default="Bitcoin", choices =['Bitcoin','Ethereum','Litecoin','Dogecoin','Bitcoin Cash']), 
        fiat: Option(str, 'One Of: USD, CAD, EUR, GBP, JPY, AUD', required=False, default='USD', choices=["USD", "EUR", "GBP", "JPY", "CAD", "AUD"])):
        fiat = fiat.strip()
        if fiat.upper() in self.fiatList:
            await ctx.respond(self.parsePriceJson(self.getPrice(crypto, fiat), fiat))
        else: await ctx.respond("Error, incorrect usage of commands. Try /help")     
    
def setup(bot):
    bot.add_cog(Crypto(bot))