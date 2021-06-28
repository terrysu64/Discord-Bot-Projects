#Date: June 27, 2021
#Author: Terry Su
#Purpose: My first discord "test bot"; playing around with the discord library
#         and various bot functions/usages in a server.


import discord

client = discord.Client()

bot_token = 'ODU4ODAzNjkwNTk2MDczNDgy.YNjdQw.h5szfvuo-_fxrOkq3wdapHfYvcA'
bot_maintenance_channel_id = 858869667865821194

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.get_channel(bot_maintenance_channel_id).send("Terry's Test Bot is ready to go!")

client.run(bot_token)
    
