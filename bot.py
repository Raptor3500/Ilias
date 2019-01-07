import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import os
import random
import youtube_dl
import nacl.secret

OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll', 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']

startup_extensions = [
  'cogs.message', 'cogs.manage', 'cogs.on_message_trolling'
]

bot = commands.Bot(command_prefix='frisk ')
bot.remove_command('help')
ownerID = "274298631517896704"
Error = 0xFF0000
messages = ['rock', 'paper', 'scissors']
client = commands.Bot(command_prefix='frisk ')
songs = asyncio.Queue()
play_next_song = asyncio.Event()



players = {}
queues = {}

def check_queue(id):
  if queues[id] != []:
    player = queues[id].pop(0)
    players[id] = player
    player.start()
  else:
    del players[id]

# To remove the help command and make your own help command
#bot.remove_command('help')

@bot.event
async def on_ready():
  print ("------")
  print ("My name is " + bot.user.name)
  print ("With the ID: " + bot.user.id)
  print ("Using discord.py v" + discord.__version__)
  print ("------")


  
  # Make me say stuff
@bot.command(pass_context=True)
async def say(ctx, *args):
    """Make me say your message"""
    if ctx.message.author.id in ownerID:
        channel = ctx.message.channel
        mesg = ' '.join(args)
        await bot.delete_message(ctx.message)
        await bot.send_typing(channel)
        await asyncio.sleep(1)
        await bot.say(mesg)
        print (ctx.message.author.id + " or " + ctx.message.author.name + " made me say '{}'".format(mesg))
        
@bot.command(pass_context=True)
async def invite(ctx):
  """Invite Me"""
  await bot.say("here's my invite link")
  await bot.say("https://discordapp.com/api/oauth2/authorize?client_id=493204973685964830&permissions=8&scope=bot")
  
@bot.command(pass_context=True)
async def help(ctx):
  embed = discord.Embed(name='help', description=None, color=0x426ef4)
  embed.set_author(name=ctx.message.author.name)
  embed.add_field(name='owner', value='not finished', inline=False)
  embed.add_field(name='cmds', value='List of commands (so far)', inline=False)
  
  await bot.say(embed=embed)
  
@bot.command(pass_context=True)
async def owner(ctx):
  embed = discord.Embed(name='owner', description=None, color=0x426ef4)
  embed.set_author(name=ctx.message.author.name)
  embed.add_field(name='playing', value='Sets my playing status', inline=False)
  embed.add_field(name='watching', value='Sets my watching status', inline=False)
  embed.add_field(name='listening', value='Sets my listening status', inline=False)
  
  await bot.say(embed=embed)
  
@bot.command(pass_context=True)
async def cmds(ctx):
  embed = discord.Embed(name='cmds', description=None, color=0x426ef4)
  embed.set_author(name=ctx.message.author.name)
  embed.add_field(name='say', value='says your message', inline=False)
  embed.add_field(name='invite', value='Invite Me', inline=False)
  
  
  await bot.say(embed=embed)

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    
@bot.command(pass_context=True)
async def info(ctx, user: discord.Member):
  
  embed = discord.Embed(title="{}'s info".format(user.name), description='Here is what I could find:', color=ctx.message.author.color)
  embed.add_field(name='Name', value='{}'.format(user.name))
  embed.add_field(name='ID', value='{}'.format(user.id), inline=True)
  embed.add_field(name='Status', value='{}'.format(user.status), inline=True)
  embed.add_field(name='Highest Role', value='<@&{}>'.format(user.top_role.id), inline=True)
  embed.add_field(name='Joined at', value='{:%d/%h/%y at %H:%M}'.format(user.joined_at), inline=True)
  embed.add_field(name='Created at', value='{:%d/%h/%y at %H:%M}'.format(user.created_at), inline=True)
  embed.add_field(name='Discriminator', value='{}'.format(user.discriminator), inline=True)
  embed.add_field(name='Playing', value='{}'.format(user.game))
  embed.set_footer(text="{}'s Info".format(user.name), icon_url='{}'.format(user.avatar_url))
  embed.set_thumbnail(url=user.avatar_url)
  
  await bot.say(embed=embed)
  
@bot.command()
async def rate(str : str):
    str = str.strip()
    number = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    if 'Xenzai' in str:
        await bot.say('Are you kidding me, Xenzai is a freaking 10/10!')
    if 'Xenzai' not in str:
        await bot.say('I rate {} a {}/10'.format(str, random.choice(number)))
        
@bot.command(pass_context=True)
async def prune(ctx, number, *args):
  if ctx.message.author.id in ownerID:
    channel = messages[0].channel
    mesg = ' '.join(args)
    mgs = [] #Empty list to put all the messages in the log
    number = int(number) #Converting the amount of messages to delete to an integer
    async for x in bot.logs_from(ctx.message.channel, limit = number):
        mgs.append(x)
    await bot.delete_messages(mgs)
    await asyncio.sleep(1)
    await bot.say(channel, "I have deleted" + (mesg) + "messages")
    await bot.delete_messages("I have deleted" + (mesg) + "messages")
    
@bot.command()
async def choose(str : str, *args):
  mesg = ' '.join(args)
  choices = [str, mesg]
  await bot.say('I choose {}'.format(random.choice(choices)))
  
@bot.command()
async def setgame(str : str, *args):
  mesg = ' '.join(args)
  str = str.strip()
  if 'playing' in str:
      await bot.change_presence(game=discord.Game(name= (mesg)))
      await bot.say("I am now playing " + mesg)
  if 'listening' in str:
      await bot.change_presence(game=discord.Game(name= mesg, type=2))
      await bot.say("I am now listening to " + mesg)
  if 'watching' in str:
      await bot.change_presence(game=discord.Game(name= mesg, type=3))
      await bot.say("I am now watching " + mesg)
      
@bot.command(pass_context=True)
async def join(ctx):
  channel = ctx.message.author.voice_channel
  await bot.join_voice_channel(channel)
  
@bot.command(pass_context=True)
async def leave(ctx):
  server = ctx.message.server
  voice_client = bot.voice_client_in(server)
  await voice_client.disconnect()
  
@bot.command(pass_context=True)
async def play(ctx, *,url):
  server = ctx.message.server
  voice_client = bot.voice_client_in(server)
  await bot.join_voice_channel(ctx.message.author.voice_channel)
  if server.id not in players:
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
    players[server.id] = player
    player.start()
  else:
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))

    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
    await bot.say('Video queued.')

  
@bot.command(pass_context=True)
async def pause(ctx):
  id = ctx.message.server.id
  players[id].pause()
  

@bot.command(pass_context=True)
async def stop(ctx):
  id = ctx.message.server.id
  players[id].stop()


@bot.command(pass_context=True)
async def resume(ctx):
  id = ctx.message.server.id
  players[id].resume()
  
@bot.command(pass_context=True)
async def secretmesg(ctx, *args):
  if ctx.message.author.id in ownerID:
    mesg = ' '.join(args)
    await bot.send_message(discord.Object(id='528295857389305858'), mesg)
    
@bot.command(pass_context=True)
async def secretdm(ctx, *args, user):
  if ctx.message.author.id in ownerID:
    mesg = ' '.join(args)
    user = discord.utils.get(bot.get_all_members(), id='462099439784427523')
    await bot.send_message(user, mesg)
  
  

  
  



      
      

      

bot.run(os.environ.get('Token'))
