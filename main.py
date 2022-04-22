import discord
import requests
import os
import json
from weather import *
#from pprint import pprint
command_prefix = "$w"

#with open('secrets.json','r') as secrets_file:
#  secrets = json.load(secrets_file)
#api_key = secrets['api_key']

client = discord.Client()

@client.event
async def on_ready():
  print("We have logged in as{0.user}".format(client))
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name='{command_prefix}[location]'))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  location = msg.replace(command_prefix,"").lower()
  if len(location)>=1:
    url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={os.getenv("api_key")}&units=metric'
    try :
      data = json.loads(requests.get(url).content)
      data = parse_data(data)
      await message.channel.send(embed = weather_message(data, location))
    except KeyError:
      await message.channel.send(embed = error_message(location))
      
    

client.run(os.getenv('TOKEN'))
