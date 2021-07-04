#Date: July 4, 2021
#Author: Terry Su
#Purpose: a cog with general user commands for Gamble Bot.py

import discord
from discord.ext import commands
import json

#GENERAL SERVER/BOT-RELATED COMMANDS

class General_Commands(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        print('Gamble Bot - General Commands has been loaded!')


    @commands.command()
    #gives information about bot
    async def info(self, ctx):
        await ctx.send("Hey! I'm the Gamble Bot! Each member starts off with $100 and can either gain or lose money as " \
                                        "you play the available games (check them out with $help)." \
                                        "Try not to go broke lol. Happy gambling! \N{MONEY BAG}")

        
    @commands.command()
    #changes server prefix
    async def change_prefix(self, ctx, *, prefix):
        with open('prefixes.json', 'r') as file:
            prefixes = json.load(file)

        prefixes[str(ctx.guild.id)] = prefix 

        with open('prefixes.json', 'w') as file:
            json.dump(prefixes, file, indent = 4)

        await ctx.send(f"Gamble Bot's server prefix changed to: {prefix}")


    @commands.command()
    #checks internet latency
    async def ping(self, ctx):
        await ctx.send(f'internet latency: {round(self.client.latency * 1000)}ms')

        
def setup(client):
    client.add_cog(General_Commands(client))
