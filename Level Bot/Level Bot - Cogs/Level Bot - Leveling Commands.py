#Date: July 11, 2021
#Author: Terry Su
#Purpose: a cog with leveling commands for Level Bot.py

import discord
from discord.ext import commands
import json
import operator

#LEVELING COMMANDS

class Leveling_Commands(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        print('Level Bot - Leveling Commands has been loaded!')


    @commands.command()
    #allows member to check their own stats
    async def level(self,ctx):

        with open('level.json', 'r') as file:
            level = json.load(file)

        embed = discord.Embed(title = "{}'s Level Stats".format(ctx.author.name))
        embed.add_field(name = 'Name', value = ctx.author.mention, inline = True)
        embed.add_field(name = 'XP', value = level[str(ctx.guild.id)][str(ctx.author)][0], inline = True)
        embed.add_field(name = 'Level', value = level[str(ctx.guild.id)][str(ctx.author)][1], inline = True)

        curr = level[str(ctx.guild.id)][str(ctx.author)][0] - ((level[str(ctx.guild.id)][str(ctx.author)][1] ** 2) * 10) #current xp relative to current level
        needed = (((level[str(ctx.guild.id)][str(ctx.author)][1]+1) ** 2) * 10) - level[str(ctx.guild.id)][str(ctx.author)][0] #xp needed to advance relative to next level
        
        embed.add_field(name = 'Progess', value = curr * ":green_square:" + needed * ":white_large_square:", inline = False)

        await ctx.channel.send(embed = embed)


    @commands.command()
    #lists out server's top 10 leaderboard (sorted by highest XP first)
    async def leaderboard(self, ctx):

        with open('level.json', 'r') as file:
            level = json.load(file)

        server = level[str(ctx.guild.id)]
        server = dict(sorted(server.items(), key=operator.itemgetter(1,0),reverse=True))

        embed = discord.Embed(title = 'Leaderboard:')
        for rank,member in enumerate(server):

            if rank == 0:
                embed.add_field(name = f'{rank+1}. {member}', value = f'level {server[member][1]}, {server[member][0]}XP \N{FIRST PLACE MEDAL}', inline = False)

            elif rank == 1:
                embed.add_field(name = f'{rank+1}. {member}', value = f'level {server[member][1]}, {server[member][0]}XP \N{SECOND PLACE MEDAL}', inline = False)

            elif rank == 2:
                embed.add_field(name = f'{rank+1}. {member}', value = f'level {server[member][1]}, {server[member][0]}XP \N{THIRD PLACE MEDAL}', inline = False)

            else:
                embed.add_field(name = f'{rank+1}. {member}', value = f'level {server[member][1]}, {server[member][0]}XP', inline = False)

                if rank == 9:
                    break

        await ctx.channel.send(embed = embed)

        return
    

        
def setup(client):
    client.add_cog(Leveling_Commands(client))
