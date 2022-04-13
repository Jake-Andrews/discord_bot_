'''
import requests
import os 
import json
from dotenv import load_dotenv
from discord.ext import tasks, commands
from twitchAPI.twitch import Twitch
from discord.utils import get


class Crypto(commands.Cog):

    def __init__(self, bot):
        load_dotenv()
        self.bot = bot
        self.client_id = os.environ['CLIENT_ID']
        self.client_secret = os.environ['CLIENT_SECRET']
        self.twitch = Twitch(self.client_secret, self.client_secret)
        #self.twitch.authenticate_app([]) #authenticate to increase rate limit
        TWITCH_STREAM_API_ENDPOINT_V5 = "https://api.twitch.tv/kraken/streams/{}"
        API_HEADERS = {
            'Client-ID': self.client_id,
            'Authorization' : 'Bearer '+ token,
        }
    
    def check_user_live(self, username):
        try:
            userid = self.twitch.get_users(logins=[username])['data'][0]['id']
            url = self.TWITCH_STREAM_API_ENDPOINT_V5.format(userid)
            try:
                req = requests.Session().get(url, headers=self.API_HEADERS)
                jsondata = req.json()
                if 'stream' in jsondata:
                    if jsondata['stream'] is not None:
                        return True
                    else:
                        return False
            except Exception as e:
                print("Error checking user: ", e)
                return False
        except IndexError:
            return False

    @tasks.loop(seconds=5)
    async def check_twitch_live(self):
        with open('database/streamers.json') as f:
            streamers = json.load(f)

        if streamers is not None: 
            notification_channel = self.bot.get_channel(960278456313204796)
            #looping through every streamer in the json file 
            for user_id, twitch_name in streamers.items():
                #returns true if user is live
                if self.check_user_live(twitch_name):
                    #grab the a list of messages from the history of the notification channel into a list (flatten)
                    messages = await notification_channel.history(limit=200).flatten()
                    combined_messages = '\t'.join(messages)
                    #the streamer has already been announced
                    if twitch_name in combined_messages:
                        break
                    #the streamer has not been announced, send message
                    else:
                        await notification_channel.send(
                            f":red_circle: **LIVE**\n{twitch_name} is now streaming on Twitch!"
                            f"\nhttps://www.twitch.tv/{twitch_name}")
                        print(f"{twitch_name} started streaming. Sending a notification.")
                #The user is not live, delete message
                else:
                    async for message in notification_channel.history(limit=200):
                        if twitch_name in message.content and "is streaming now" in message.content:
                            await message.delete()
    
    @check_twitch_live.before_loop
    async def before_check_live(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Crypto(bot))
'''