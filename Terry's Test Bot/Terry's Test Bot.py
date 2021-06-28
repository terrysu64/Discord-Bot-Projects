#Date: June 27, 2021
#Author: Terry Su
#Purpose: My first discord "test bot"; playing around with the discord library
#         and various bot functions/usages in a server.

#Invite link: https://discord.com/api/oauth2/authorize?client_id=858803690596073482&permissions=0&scope=bot

import discord

client = discord.Client()

# bot_token = 
# bot_maintenance_channel_id = 

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.get_channel(bot_maintenance_channel_id).send("Terry's Test Bot is ready to go!")

client.run(bot_token)
    
