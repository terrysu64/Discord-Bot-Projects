#Date: July 11, 2021
#Author: Terry Su
#Purpose: a simpling levelling bot with xp tracking for server members;
#         start by using $help and $info in your discord server to learn
#         more about this bot!

#Invite link: https://discord.com/api/oauth2/authorize?client_id=863771363146989628&permissions=8&scope=bot

import discord
from discord.ext import commands
import os
import json
import math


#INITIALIZING BOT PROPRETIES AND OTHER GLOBAL VARIABLES

def set_prefix(client, message):
    
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)

    return prefixes[str(message.guild.id)]

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = set_prefix, intents = intents)
bot_token = ''
bot_maintenance_channel_id = 


#GENERAL EVENTS

@client.event
async def on_ready():

    print('Level Bot is now online!')
    await client.get_channel(bot_maintenance_channel_id).send('Level Bot is updated and ready to go!')
    await client.change_presence(activity = discord.Game('with bottles o enchanting'))

 
@client.event
#when Level Bot joins a server, all members start with 0 XP at level 0 by default;
async def on_guild_join(guild):

    print(f'Level Bot has joined: {guild}')
    await client.change_presence(activity = discord.Game('with bottles o enchanting'))


    #Setting up server prefix
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)

    prefixes[str(guild.id)] = '#' 

    with open('prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent = 4)

    
    #Distributing money to members
    with open('level.json', 'r') as file:
        level = json.load(file)

    level[str(guild.id)] = {}

    for member in guild.members:
        level[str(guild.id)][str(member)] = [0,0] #XP, Level 

    with open('level.json', 'w') as file:
        json.dump(level, file, indent = 4)



@client.event
#when Level Bot leaves a server, all the server's data is wiped out  
async def on_guild_remove(guild):

    print(f'Level Bot has left: {guild}')

    #removing server prefix
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent = 4)


    #removing money data
    with open('level.json', 'r') as file:
        level = json.load(file)

    level.pop(str(guild.id))

    with open('level.json', 'w') as file:
        json.dump(level, file, indent = 4)


@client.event
#when a member joins a server with Level Bot, they are given the starting XP and level
async def on_member_join(member):

    with open('level.json', 'r') as file:
        level = json.load(file)

    level[str(member.guild.id)][str(member)] = [0,0]

    with open('level.json', 'w') as file:
        json.dump(level, file, indent = 4)


@client.event
#when a member leaves a server with Level Bot, their data is erased
async def on_member_remove(member):

    with open('level.json', 'r') as file:
        level = json.load(file)

    level[str(member.guild.id)].pop(str(member))

    with open('level.json', 'w') as file:
        json.dump(level, file, indent = 4)


@client.event
#when a member sends a message they gain 1 XP (quadratic leveling algorithm: level^2 * 10 = XP needed -----> level = sqrt(XP/10))
async def on_message(message):

    await client.process_commands(message)
    if message.author!= client.user:

        with open('level.json', 'r') as file:
            level = json.load(file)

        level[str(message.guild.id)][str(message.author)][0] += 1

        hold = level[str(message.guild.id)][str(message.author)][1]
        level[str(message.guild.id)][str(message.author)][1] = int(math.sqrt(level[str(message.guild.id)][str(message.author)][0] / 10))
        new = level[str(message.guild.id)][str(message.author)][1]

        if new != hold:
            await message.channel.send(f'Congrats {message.author.mention}! You just advanced to level {new} \N{PARTY POPPER}') 
            
        with open('level.json', 'w') as file:
            json.dump(level, file, indent = 4)
        

#GENERAL ERROR HANDLING
        
@client.event
async def on_command_error(ctx, error):
    await ctx.send('ah looks like we encountered an error with your command; make sure your command/arguments are valid... \N{WARNING SIGN}')


#LOADING COGS
        
for filename in os.listdir('./Level Bot - Cogs'):  
    if filename.endswith('.py'):
        client.load_extension(f'Level Bot - Cogs.{filename[:-3]}')


client.run(bot_token)
