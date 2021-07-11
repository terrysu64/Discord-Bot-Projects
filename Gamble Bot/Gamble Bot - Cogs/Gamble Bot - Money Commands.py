#Date: July 4, 2021
#Author: Terry Su
#Purpose: a cog with personal money-relaterd action commands for Gamble Bot.py

import discord
from discord.ext import commands
import json
import operator

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

        with open('money.json', 'r') as file:
            money = json.load(file)
   
        await ctx.send(f'{ctx.author}: ${money[str(ctx.guild.id)][str(ctx.author)]}')
        return


   @commands.command()
    #lists out server's top 10 leaderboard (sorted by richest first)
    async def leaderboard(self, ctx):

        with open('money.json', 'r') as file:
            money = json.load(file)

        server = money[str(ctx.guild.id)]
        server = dict(sorted(server.items(), key=operator.itemgetter(1),reverse=True))

  
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
