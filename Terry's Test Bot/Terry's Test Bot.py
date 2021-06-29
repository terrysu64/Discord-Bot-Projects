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
    
    await client.process_commands(message) #lets bot process both commands and messages
    global times_called
    
    if message.author != client.user: #don't respond if the author is ourselves

        if message.content == '//help': #gives some info about our bot
            await message.channel.send('Hey! This is a test bot! No specific purpose, just used to play around with the Discord library and its functions!')
        
        elif message.content == '//roll dice': #rolls a dice 
            await message.channel.send('you rolled a ' + str(random.randint(1,6)) + ' ' + '\N{GAME DIE}') #use /N{emoji name} to send emojis


@client.command()
#checks our bot's network latency
async def ping(ctx): #ctx = context
    await ctx.send(f'pong! {round(client.latency * 1000)}ms')


@client.command(aliases = ['8ball', 'question']) #aliases are exchangable user prompts that call this command
#gives user random answer to a question
async def random_ans(ctx, *, question): # * lets us take in multiple arguments as one 
    
    answers = ['definetly!',
               'probably',
               'um maybe, ask again later...',
               'not very likely',
               'impossible']
    await ctx.send(f'Question: {question} \nAnswer: {random.choice(answers)}')


@client.command()
#clears a certain amount of messages from a channel
async def clear(ctx, amount = 1):

    if amount < 0:
        await ctx.channel.send('invalid clear amount')
                               
    await ctx.channel.purge(limit = amount)


@client.command()
#kicking a member
async def kick(ctx, member: discord.Member, *, reason = None):
    await member.kick(reason = reason)
    await ctx.channel.send(f'{member} was kicked. we hope he enjoys his next 24 hours')


@client.command()
#banning a member
async def ban(ctx, member: discord.Member, *, reason = None):

    try:
        await member.ban(reason = reason)
        await ctx.channel.send(f'{member} was banned.')

    except discord.errors.Forbidden: #in the scenrario where the user to be banned holds a higher role than the user who typed the command
        await ctx.channel.send('you lack power')


@client.command()
#unbanning a member
async def unban(ctx, *, member):
    
    banned_users = await ctx.guild.bans() #an iterative
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:

        user = ban_entry.user

        if (user.name,user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user.name}#{user.discriminator} has been disciplined and unbanned')
            return




    

client.run(bot_token) #initiates our bot on discord
    

