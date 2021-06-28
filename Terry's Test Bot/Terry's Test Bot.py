#Date: June 27, 2021
#Author: Terry Su
#Purpose: My first discord "test bot"; playing around with the discord library
#         and various bot functions/usages in a server.

#all of the bot events will be written with the help of the discord library

#Invite link: https://discord.com/api/oauth2/authorize?client_id=858803690596073482&permissions=0&scope=bot

import discord
from discord.ext import commands
import random

client = discord.Client()
client = commands.Bot(command_prefix = '//') #???

bot_token = '' #the bot's token is similar to a password to directly access the bot on
                                                                          #discord from our code
bot_maintenance_channel_id = 
times_used = 0


@client.event
#set's up or updates our bot
async def on_ready():
    
    print('We have logged in as {0.user}'.format(client))
    await client.get_channel(bot_maintenance_channel_id).send("Terry's Test Bot is updated and ready to go!") #sends message to bot-maintenance channel


@client.event
#responds to "//" command messages for our bot
async def on_message(message):

    if message.author != client.user: #don't respond if the author is ourselves

        if message.content == '//help': #gives some info about our bot
            await message.channel.send('Hey! This is a test bot! No specific purpose, just used to play around with the Discord library and its functions!')
            times_used += 1
        
        elif message.content == '//roll dice': #rolls a dice 
            await message.channel.send('you rolled a ' + str(random.randint(1,7)) + ' ' + '\N{GAME DIE}') #use /N{emoji name} to send emojis
            times_used += 1



        

client.run(bot_token) #initiates our bot on discord
    

