#Date: July 4, 2021
#Author: Terry Su
#Purpose: a cog with personal money-relaterd action commands for Gamble Bot.py

import discord
from discord.ext import commands
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
import os
database_password = os.environ.get("DATABASE_PASSWORD")

cluster = MongoClient(f'mongodb+srv://terrysu64:{database_password}@discord-bots.ho9kj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["gamble-bot"]
money_collection = db["prefixes"]

#MONEY ACTION COMMANDS

class Money_Commands(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        print('Gamble Bot - Money Commands has been loaded!')


    @commands.command()
    #allows member to lookup how much money they have in a server
    async def rich(self, ctx):

        result = money_collection.find_one({"guild": str(ctx.guild.id), "member": str(ctx.author)})
        print(result)
        await ctx.send(f'{ctx.author}: ${result["money"]}')
        return


    @commands.command()
    #lists out server's top 10 leaderboard (sorted by richest first)
    async def leaderboard(self, ctx):

        server = money_collection.find({"guild": str(ctx.guild.id)})
        server.sort(key=lambda x:-x["money"])

        for rank,member in enumerate(server):

            if rank == 0:
                await ctx.send(f'{rank+1}. {member}: ${server[member]} \N{FIRST PLACE MEDAL}')

            elif rank == 1:
                await ctx.send(f'{rank+1}. {member}: ${server[member]} \N{SECOND PLACE MEDAL}')

            elif rank == 2:
                await ctx.send(f'{rank+1}. {member}: ${server[member]} \N{THIRD PLACE MEDAL}')

            else:
                await ctx.send(f'{rank+1}. {member}: ${server[member]}')

                if rank == 9:
                    break
        return


def setup(client):
    client.add_cog(Money_Commands(client))
