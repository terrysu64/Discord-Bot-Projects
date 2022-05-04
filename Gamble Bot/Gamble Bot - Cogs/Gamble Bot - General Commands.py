#Date: July 4, 2021
#Author: Terry Su
#Purpose: a cog with general user commands for Gamble Bot.py

import discord
from discord.ext import commands
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
import os
database_password = os.environ.get("DATABASE_PASSWORD")

cluster = MongoClient(f'mongodb+srv://terrysu64:{database_password}@discord-bots.ho9kj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["gamble-bot"]
prefixes_collection = db["prefixes"]

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

        prefixes_collection.update_one({"guild": str(ctx.guild.id)}, {"$set": {"prefix":prefix}})

        await ctx.send(f"Gamble Bot's server prefix changed to: {prefix}")


    @commands.command()
    #checks internet latency
    async def ping(self, ctx):
        await ctx.send(f'internet latency: {round(self.client.latency * 1000)}ms')

        
def setup(client):
    client.add_cog(General_Commands(client))
