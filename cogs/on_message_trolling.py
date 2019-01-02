import discord
import requests
import json

user = 'rZuTJlFKDZF5oi0T'
key = 'jiaN5JDdXrvjRNFng4t9rlMF47pjazst'

class on_message_trolling():
    def __init__(self, bot):
        self.bot = bot
        
        async def on_message(self, message, ctx):
            user = ctx.message.author
            mesg = ctx.message.content
            print(f'{user} said "{mesg}"')
            botmesg = input()
            await bot.send_message(channel, (botmesg))
            if ctx.message.author == self.bot.user:
                return
            
            
            
print('Starting Trolling Process...')
def setup(bot):
    bot.add_cog(on_message_trolling(bot))
