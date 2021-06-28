#Date: June 27, 2021
#Author: Terry Su
#Purpose: My first discord "test bot"; playing around with the discord library
#         and various bot functions/usages in a server.

#all of the bot events will be written with the help of the discord library

#Invite link: https://discord.com/api/oauth2/authorize?client_id=858803690596073482&permissions=0&scope=bot

import discord
from discord.ext import commands
import random

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix= '//' , intents = intents)

bot_token = '' #the bot's token is similar to a password to directly access the bot on
                                                                          #discord from our code
bot_maintenance_channel_id = 
times_called = 0

@client.event
#set's up or updates our bot
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.get_channel(bot_maintenance_channel_id).send("Terry's Test Bot is updated and ready to go!") #sends message to bot-maintenance channel

@client.event
#notifies us in the shell when users have joined the server
async def on_member_join(member):
    print(f'{member} has joined the server')

@client.event
#notifies us in the shell when users have left the server
async def on_member_remove(member):
    print(f'{member} has left the server')

@client.event
#responds to "//" command messages for our bot
async def on_message(message):
    global times_called
    if message.author != client.user: #don't respond if the author is ourselves

        if message.content == '//help': #gives some info about our bot
            await message.channel.send('Hey! This is a test bot! No specific purpose, just used to play around with the Discord library and its functions!')
            times_called += 1
            print("Terry's Test Bot was called " + str(times_called) + ' ' + 'times.')
        
        elif message.content == '//roll dice': #rolls a dice 
            await message.channel.send('you rolled a ' + str(random.randint(1,6)) + ' ' + '\N{GAME DIE}') #use /N{emoji name} to send emojis
            times_called += 1
            print("Terry's Test Bot was called " + str(times_called) + ' ' + 'times.')

@client.command() #NOT WORKING
async def ping(ctx): #ctx = context
    await ctx.send('hi')





client.run(bot_token) #initiates our bot on discord
    

