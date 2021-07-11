#Date: July 11, 2021
#Author: Terry Su
#Purpose: a cog with general user commands for Level Bot.py

import discord
from discord.ext import commands
import json

#GENERAL SERVER/BOT-RELATED COMMANDS

class General_Commands(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        print('Level Bot - General Commands has been loaded!')


    @commands.command()
    #gives information about bot
    async def info(self, ctx):
        await ctx.send("Hey! I'm the Level Bot! Each member starts off with 0 XP at level 0, the more messages you send in this "
                                        "server the higher your level will be! " \
                                        "Check out bot commands with #help. " \
                                        "Enjoy your leveling journey! \N{SMILING FACE WITH SMILING EYES}")

        
    @commands.command()
    #changes server prefix
    async def change_prefix(self, ctx, *, prefix):
        with open('prefixes.json', 'r') as file:
            prefixes = json.load(file)

        prefixes[str(ctx.guild.id)] = prefix 

        with open('prefixes.json', 'w') as file:
            json.dump(prefixes, file, indent = 4)

        await ctx.send(f"Level Bot's server prefix changed to: {prefix}")


    @commands.command()
    #checks internet latency
    async def ping(self, ctx):
        await ctx.send(f'internet latency: {round(self.client.latency * 1000)}ms')

        
def setup(client):
    client.add_cog(General_Commands(client))
