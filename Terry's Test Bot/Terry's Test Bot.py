#Date: June 27, 2021
#Author: Terry Su
#Purpose: My first discord "test bot"; playing around with the discord library
#         and various bot functions/usages in a server.

#all of the bot events will be written with the help of the discord library

#Invite link: https://discord.com/api/oauth2/authorize?client_id=858803690596073482&permissions=0&scope=bot

import discord
from discord.ext import commands
from discord.ext import tasks
from itertools import cycle
import os
import random
import json

def get_prefix(client, message):
    
    #getting custom prefixes for servers
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)

    return prefixes[str(message.guild.id)]

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = get_prefix , intents = intents)

bot_token = '' #the bot's token is similar to a password to directly access the bot on
                                                                          #discord from our code
bot_maintenance_channel_id = 
txrry_id = 


@client.event
#set's up or updates our bot
async def on_ready():
    
    print('We have logged in as {0.user}'.format(client))
    await client.get_channel(bot_maintenance_channel_id).send("Terry's Test Bot is updated and ready to go!") #sends message to bot-maintenance channel
    
    await client.change_presence(status = discord.Status.idle)
    await client.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = 'YouTube'))
    #there are a range of prescences/status and activities we could initialize for our bot
                                                                                                                  

@client.event
#sets default command prefix to '//'
async def on_guild_join(guild):

    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)

    prefixes[str(guild.id)] = '//' 

    with open('prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent = 4)


@client.event
#removing command prefix when bot leaves a server
async def on_guild_remove(guild):

    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent = 4)


@client.command()
#changing custom bot prefix
async def change_prefix(ctx, *, prefix):

    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)

    prefixes[str(ctx.guild.id)] = prefix 

    with open('prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent = 4)

    await ctx.send(f'prefix changed to: {prefix}')

@client.event
#notifies us in the shell when users have joined the server
async def on_member_join(member):
    print(f'{member} has joined the server')


@client.event
#notifies us in the shell when users have left the server
async def on_member_remove(member):
    print(f'{member} has left the server')


@client.event
#responds to "//" command messages for our bot (just testing them as events)
async def on_message(message):
    
    await client.process_commands(message) #lets bot process both commands and messages
    global times_called
    
    if message.author != client.user: #don't respond if the author is ourselves

        if message.content == '//help': #gives some info about our bot
            await message.channel.send('Hey! This is a test bot! No specific purpose, just used to play around with the Discord library and its functions!')
        
        elif message.content == '//roll dice': #rolls a dice 
            await message.channel.send(f'you rolled a {random.randint(1,6)} ' + '\N{GAME DIE}') #use '/N{emoji name}' to send emojis


@client.event
#general error handling
async def on_command_error(ctx, error):

    await ctx.send('ah looks like we encountered an error with your command ' + '\N{FACE WITH OPEN MOUTH}')
    
    if isinstance(error, commands.MissingRequiredArgument): #we could also specify the specific error if we want
        await ctx.send('missing required arguments!')


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
@commands.has_permissions(manage_messages = True)
#clears a certain amount of messages from a channel (only enabled for admin with message managing permissions)
async def clear(ctx, amount: int):                 
    await ctx.channel.purge(limit = amount)


@clear.error
#command-specific error handling
async def clear_error(ctx, error):
    await ctx.send('please specify an amount of messages to delete or ask admin for permission to use //clear')

    
#example of custom command that only I can use
def is_it_me(ctx):
    return ctx.author.id == txrry_id

@client.command()
@commands.check(is_it_me)
async def custom_test(ctx):
    await ctx.send(f'hey im {ctx.author}, the creator of this bot')

    
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


@client.command()
#loading cogs manually (files of code that are loaded onto our main class/this file; helps us organize our bot program instead of jamming everything on here)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
#unloading cogs manually
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


status = cycle(['Minecraft','Fortnite','Slither.io', 'Clash Royale'])
@tasks.loop(seconds = 10)
#changes bots status every 5 seconds
async def change_status():
    await client.change_presence(activity = discord.Game(next(status)))


@client.command()
#start looping bot status
async def start_status_loop(ctx):
    await ctx.send('status looping has begun')
    change_status.start()


@client.command()
#ends bot status loop
async def end_status_loop(ctx):
    await ctx.send('status looping has ended')
    await client.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = 'YouTube'))


#loads all cogs by default when we start up the bot (could also be made into a command)
for filename in os.listdir("./Terry's Test Bot - Cogs"): #looks for python files 
    if filename.endswith('.py'):
        client.load_extension(f"Terry's Test Bot - Cogs.{filename[:-3]}")



client.run(bot_token) #initiates our bot on discord
    

    


    

    

