#Date: June 27, 2021
#Author: Terry Su
#Purpose: My first discord "test bot"; playing around with the discord library
#         and various bot functions/usages in a server.

#all of the bot events will be written with the help of the discord library

#Invite link: https://discord.com/api/oauth2/authorize?client_id=858803690596073482&permissions=0&scope=bot

import discord

client = discord.Client()

bot_token = 'ODU4ODAzNjkwNTk2MDczNDgy.YNjdQw.h5szfvuo-_fxrOkq3wdapHfYvcA' #the bot's token is similar to a password to directly access the bot on
                                                                          #discord from our code
bot_maintenance_channel_id = 858869667865821194

@client.event
async def on_ready(): #set's up or updates our bot
    print('We have logged in as {0.user}'.format(client))
    await client.get_channel(bot_maintenance_channel_id).send("Terry's Test Bot is ready to go!") #sends message to bot-maintenance channel

client.run(bot_token) #initiate's our bot on discord
    
