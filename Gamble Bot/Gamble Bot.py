#Date: July 4, 2021
#Author: Terry Su
#Purpose: Bot with various money gambling functions for members to use;
#         start by using $help and $info in your discord server to learn
#         more about this bot!

#Invite link: https://discord.com/api/oauth2/authorize?client_id=860571788650872854&permissions=1074261056&scope=bot

import discord
from discord.ext import commands
from discord.ext import tasks
import os
import random
import json

#INITIALIZING BOT PROPRETIES AND OTHER GLOBAL VARIABLES

def set_prefix(client, message):
    
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)

    return prefixes[str(message.guild.id)]

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = set_prefix, intents = intents)
bot_token = 
bot_maintenance_channel_id = 


# GENERAL EVENTS

@client.event
async def on_ready():

    print('Gamble Bot is now online!')
    await client.get_channel(bot_maintenance_channel_id).send('Gamble Bot is updated and ready to go!')
    await client.change_presence(status = discord.Status.idle, activity = discord.Game('with money'))

 
@client.event
#when Gamble Bot joins a server, all members start with $100 by default;
async def on_guild_join(guild):

    print(f'Gamble Bot has joined: {guild}')
    await client.change_presence(status = discord.Status.idle, activity = discord.Game('with money'))


    #Setting up server prefix
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)

    prefixes[str(guild.id)] = '$' 

    with open('prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent = 4)

    
    #Distributing money to members
    with open('money.json', 'r') as file:
        money = json.load(file)

    money[str(guild.id)] = {}

    for member in guild.members:
        money[str(guild.id)][str(member)] = 100 

    with open('money.json', 'w') as file:
        json.dump(money, file, indent = 4)



@client.event
#when Gamble Bot leaves a server, all the server's data is wiped out  
async def on_guild_remove(guild):

    print(f'Gamble Bot has left: {guild}')

    #removing server prefix
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent = 4)


    #removing money data
    with open('money.json', 'r') as file:
        money = json.load(file)

    money.pop(str(guild.id))

    with open('money.json', 'w') as file:
        json.dump(money, file, indent = 4)


@client.event
#when a member joins a server with Gamble Bot, they are given the starting $100
async def on_member_join(member):

    with open('money.json', 'r') as file:
        money = json.load(file)

    money[str(member.guild.id)][str(member)] = 100

    with open('money.json', 'w') as file:
        json.dump(money, file, indent = 4)


@client.event
#when a member leaves a server with Gamble Bot, their data is erased
async def on_member_remove(member):

    with open('money.json', 'r') as file:
        money = json.load(file)

    money[str(member.guild.id)].pop(str(member))

    with open('money.json', 'w') as file:
        json.dump(money, file, indent = 4)


#GENERAL ERROR HANDLING
        
@client.event
async def on_command_error(ctx, error):
    await ctx.send('ah looks like we encountered an error with your command; make sure your command/arguments are valid... \N{WARNING SIGN}')


#LOADING COGS
        
for filename in os.listdir('./Gamble Bot - Cogs'):  
    if filename.endswith('.py'):
        client.load_extension(f'Gamble Bot - Cogs.{filename[:-3]}')


client.run(bot_token)
