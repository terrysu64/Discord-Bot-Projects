#Date: July 4, 2021
#Author: Terry Su
#Purpose: Bot with various money gambling functions for members to use;
#         start by using $help and $info in your discord server to learn
#         more about this bot!

#Invite link: https://discord.com/api/oauth2/authorize?client_id=860571788650872854&permissions=1074261056&scope=bot

import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
import os
import json
from pymongo import MongoClient

#INITIALIZING 

bot_token = os.environ.get("BOT_TOKEN")
bot_maintenance_channel_id = os.environ.get("MAINTENANCE_CHANNEL")
database_password = os.environ.get("DATABASE_PASSWORD")

cluster = MongoClient(f'mongodb+srv://terrysu64:{database_password}@discord-bots.ho9kj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["gamble-bot"]
prefixes_collection = db["prefixes"]
money_collection = db["money"]

def set_prefix(client, message):
    
    result = prefixes_collection.find_one({"guild":str(message.guild.id)})

    return result["prefix"]

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = set_prefix, intents = intents)

# GENERAL EVENTS

@client.event
async def on_ready():

    print('Gamble Bot is now online!')
    await client.get_channel(int(bot_maintenance_channel_id)).send('Gamble Bot is updated and ready to go!')
    await client.change_presence(status = discord.Status.idle, activity = discord.Game('with money'))

 
@client.event
#when Gamble Bot joins a server, all members start with $100 by default;
async def on_guild_join(guild):

    print(f'Gamble Bot has joined: {guild}')
    await client.change_presence(status = discord.Status.idle, activity = discord.Game('with money'))

    #Setting up server prefix
    post = {"guild": str(guild.id), "prefix": "$"}
    prefixes_collection.insert_one(post)

    
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
    delete = {"guild":str(guild.id)}
    prefixes_collection.delete_one(delete)

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
        
# @client.event
# async def on_command_error(ctx, error):
#     await ctx.send('ah looks like we encountered an error with your command; make sure your command/arguments are valid... \N{WARNING SIGN}')


#LOADING COGS
        
for filename in os.listdir('./Gamble Bot - Cogs'):  
    if filename.endswith('.py'):
        client.load_extension(f'Gamble Bot - Cogs.{filename[:-3]}')


client.run(bot_token)
