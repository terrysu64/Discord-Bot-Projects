#Date: June 29, 2021
#Author: Terry Su
#Purpose: a cog for Terry's Test Bot.py

import discord
from discord.ext import commands

class Extra_Commands(commands.Cog):

    def __init__(self, client):
        self.client = client

    #event
    @commands.Cog.listener()
    async def on_ready(self):
        print("Terry's Test Bot - extra commands has been loaded!")

    #command
    @commands.command()
    async def test(self, ctx):
        await ctx.send('testing testing 1 2 3, this cog is ready to go!')

def setup(client):
    client.add_cog(Extra_Commands(client))
   
