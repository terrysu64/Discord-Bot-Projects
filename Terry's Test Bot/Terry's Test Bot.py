#Date: June 27, 2021
#Author: Terry Su
#Purpose: My first discord "test bot"; playing around with the discord library
#         and various bot functions/usages in a server.


import discord

client = discord.Client()

# bot_token = 
# bot_maintenance_channel_id = 

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.get_channel(bot_maintenance_channel_id).send("Terry's Test Bot is ready to go!")

client.run(bot_token)
    
