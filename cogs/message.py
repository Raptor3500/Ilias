import discord
import requests
import json

user = 'rZuTJlFKDZF5oi0T'
key = 'jiaN5JDdXrvjRNFng4t9rlMF47pjazst'

class message():
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if 'pervert' in message.content:
            await self.bot.send_message(message.channel, " *attempts to kill the perv* ")
            
        if not message.author.bot and (message.server == None or self.bot.user in message.mentions):
            await self.bot.send_typing(message.channel)
            txt = message.content.replace(message.server.me.mention,'') if message.server else message.content
            r = json.loads(requests.post('https://cleverbot.io/1.0/ask', json={'user':user, 'key':key, 'nick':'claire', 'text':txt}).text)
            if r['status'] == 'success':
                await self.bot.send_message(message.channel, r['response'] )
                



print('Starting CleverBot...')
requests.post('https://cleverbot.io/1.0/create', json={'user':user, 'key':key, 'nick':'claire'})
def setup(bot):
    bot.add_cog(message(bot))
