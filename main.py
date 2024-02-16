print("[ ! ] Loading Modules...\n")
import json
import os
try: os.system("pip install -r ./requirements.txt")
except: pass
try: os.system("py -m pip install -r ./requirements.txt")
except: os.system("python -m pip install -r ./requirements.txt")

import discord
import random
import string
from typing import (Coroutine, Literal , Union)
from keep_alive import keep_alive
from discord import DMChannel
from discord.ext import commands

#Export bot prefix and token from .env file or config.json file.
prefix = os.getenv('prefix') or json.load(open("config.json"))["prefix"]
token = os.getenv('token') or json.load(open("config.json"))["token"]

#Export valid channels id from .env file or config.json file.
valid_channels = os.getenv('valid_channels') or json.load(open("config.json"))["valid_channels"]

#Get all intents for discord library.
intents = discord.Intents().all()
client = commands.Bot(command_prefix = prefix, intents = intents) 

#Remove help command.
client.remove_command('help')
  
#Alert on console when your bot is online on discord and add activity for bot.
@client.event
async def on_ready() -> Union[Coroutine , Literal[None]]:
    activity = "Generating Nitro"
    await client.change_presence(
      status = discord.Status.do_not_disturb, 
      activity = discord.Game(
        name = activity, 
        type = 3
      )
    )
    print(fr'Your bot is ready for now and logged in to the {client.user}')

#Generate nitro code command.
@client.command()
async def gen(ctx) -> Union[Coroutine , Literal[None]]:
    url = "https://discord.gift/"
    text = "**Your Nitro Code=>** "
    wrong = "you can't use this command in here."
    nitroEmbed = discord.Embed(
      title = "Your Nitro Code Is Ready", 
      url = "https://discord.gg/FareService", 
      description = "**I have sent you an unchecked Discord nitro code!**\n> Check Your Dm's!\n> use again the command: " + fr"`{prefix}gen`",
      color = discord.Color.from_rgb(5, 195, 221)
    )
    nitroEmbed.set_footer(
     text = "TomAbi"
    )
    user = await client.fetch_user(fr"{ctx.author.id}")
    chars = string.ascii_letters + string.digits
    length = random.choice(list([ 8, 16, 24 ]))
    code = "".join(random.choices(chars, k = length))
    if any(x == ctx.channel.id for x in valid_channels):
     await ctx.reply(embed =  nitroEmbed, mention_author = False)
     await DMChannel.send(user, fr"{text}{url}{code}")
    else: 
      channels = []
      for id in valid_channels:
        if discord.utils.get(ctx.guild.channels, id = id):
          channels.append(fr"<#{id}>")

      channel_list = ", ".join(channels)
      if channels:
        await ctx.reply(wrong + "\n" + fr"Whitelist channels in guild: {channel_list}")
      else: 
        await ctx.reply(wrong)
      
#Password generate command
@client.command()
async def genpass(ctx, length = 8) -> Union[Coroutine , Literal[None]]:
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ""
    if not length:
      length = 16
    for index in range(length):
        password = password + random.choice(characters)
    passwor_dembed = discord.Embed(
      title = "Your Password Is Ready",
      description = fr"**this is your generated password: ||`{password}`||**",
      color = discord.Color.orange()
    )
    await ctx.reply(embed = passwor_dembed, mention_author = False)
    
#Send user avatar command.
@client.command()
async def avatar(ctx, member : discord.Member=None) -> Union[Coroutine , Literal[None]]:
    if not member:
      member = ctx.author
    av_emb = discord.Embed(
        title = "Avatar Link 🔗",
        url = member.avatar_url,
        color = discord.Color.random()
    )
    av_emb.set_author(
        name = fr"{member}",
        icon_url = member.avatar_url
    )
    av_emb.set_footer(
        text = fr"Requested by {ctx.author}",
        icon_url = ctx.author.avatar_url
    )
    av_emb.set_image(
      url = member.avatar_url
    )
    await ctx.reply(embed = av_emb, mention_author = False)

#Help command.
@client.command()
async def help(ctx) -> Union[Coroutine , Literal[None]]:
  helpEmbed = discord.Embed(
    title = "Nitro Bot Help Command", 
    url = "https://discord.gg/fareservice", 
    description = "this is bot help embed, and you can see all bot commands.", 
    color = discord.Color.random()
  )
  helpEmbed.set_footer(
    text = "TomAbi",
    icon_url = "you Photo"
  )
  helpEmbed.add_field(
    name = fr"**{prefix}gen**" , 
    value = "generating a nitro code for you.",
    inline = True
  )
  helpEmbed.add_field(
    name = fr"**{prefix}avatar [mention-user]**", 
    value = "send target user avatar.", 
    inline = True
  )
  helpEmbed.add_field(
    name = fr"**{prefix}genpass [number]**", 
    value = "generating password with custom length.", 
    inline = True
  )
  await ctx.reply(embed = helpEmbed, mention_author = False)

#Import keep_alive function from keep_alive.py file.
keep_alive()

#Login in to the bot
try:
 client.run(token)
except AssertionError as error:
  print("Doesn't login in to the bot because has getting an error.\n")
  print(error)
