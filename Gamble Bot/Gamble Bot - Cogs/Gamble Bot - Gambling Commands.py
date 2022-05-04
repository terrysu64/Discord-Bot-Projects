#Date: July 4, 2021
#Author: Terry Su
#Purpose: a cog with gambling action commands for Gamble Bot.py

import discord
from discord.ext import commands
import json
import random
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
import os
database_password = os.environ.get("DATABASE_PASSWORD")

cluster = MongoClient(f'mongodb+srv://terrysu64:{database_password}@discord-bots.ho9kj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["gamble-bot"]
money_collection = db["prefixes"]

#GAMBLING ACTION COMMANDS

class Gambling_Commands(commands.Cog):

    def __init__(self, client):
        self.client = client


    def money_check(self, ctx): #checks a member's money in a specific server
        
        result = money_collection.find_one({"guild": str(ctx.guild.id), "member": str(ctx.author)})
        if result and result["member"] <= 0: return True
        return False
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Gamble Bot - Gambling Commands has been loaded!')


    @commands.command()
    #lets broke member borrow money from bank if they guess the right number from 1-4
    async def borrow(self, ctx):

        check = self.money_check(ctx)
        if check == True:
            await ctx.send("Ummm looks like you still got some coins in your pockets...go to gamble some more and come back when you're impoverished.")
            return

        num = random.randint(1,4)
        await ctx.send('im thinking of a number from 1-4, which is it...?')

        #This will make sure that user responses to Gamble Bot will only be registered if the following
        #conditions are met:
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        
        msg = await self.client.wait_for('message', check=check)
        
        if msg.content.lower() == str(num):

            #change data within money.json
            money_collection.update_one({"guild": str(ctx.guild.id), "member": str(ctx.author)}, {"$set": {"money": 5}})

        else:
            await ctx.send('incorrect! try again later...')

    @commands.command()
    #rolls dice with 6 possible outcomes
    async def roll_dice(self, ctx):

        outcomes = {1: -30, 2: -20, 3: -30, 4: 10, 5: 20, 6: 30}

        check = self.money_check(ctx)
        if check == False:
            await ctx.send("Ummm looks like you're broke...go to the bank first lmao.")
            return
        
        result = random.randint(1,6)

        #change data within money.json
        result = money_collection.find_one({"guild": str(ctx.guild.id), "member": str(ctx.author)})
        money_collection.update_one({"guild": str(ctx.guild.id), "member": str(ctx.author)}, {"$set": {"money": result["money"]+5}})

        await ctx.send(f'you rolled a {result} \N{GAME DIE}')
        
        #tell member their result
        if result == 1 or result == 2 or result == 3:
            await ctx.send(f'RIP you lost ${str(outcomes[result])[1:]} \N{GRIMACING FACE}')
        
        else:
            await ctx.send(f'Nice one! You won ${str(outcomes[result])} \N{MONEY-MOUTH FACE}')


    @commands.command()
    #lets member bet heads or tails
    async def flip_coin(self, ctx):

        check = self.money_check(ctx)
        if check == False:
            await ctx.send("Ummm looks like you're broke...go to the bank first lmao.")
            return

        await ctx.send('i just flipped...heads or tails...?')
        responses = ['Heads', 'heads', 'HEADS', 'H', 'h','Tails', 'tails', 'TAILS', 'T', 't']

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        
        msg = await self.client.wait_for('message', check=check)
        
        if msg.content.lower() not in responses:
            await ctx.send("you're answer is invalid")
            
        else:
            result = random.randint(0,1)
            
            #change data within money.json
            result = money_collection.find_one({"guild": str(ctx.guild.id), "member": str(ctx.author)})
            if result == 0:
                money_collection.update_one({"guild": str(ctx.guild.id), "member": str(ctx.author)}, {"$set": {"money": result["money"]+10}})

            else:
                money_collection.update_one({"guild": str(ctx.guild.id), "member": str(ctx.author)}, {"$set": {"money": result["money"]-10}})

            #tell member their result
            if result == 1:
                await ctx.send(f'RIP you lost $10 \N{GRIMACING FACE}')
            
            else:
                await ctx.send(f'Nice one! You won $10 \N{MONEY-MOUTH FACE}')


    @commands.command()
    #allows members to bet a certain amount of money with 1/4 winning chance
    async def raw_bet(self, ctx, *, amount):

        check = self.money_check(ctx)
        if check == False:
            await ctx.send("Ummm looks like you're broke...go to the bank first lmao.")
            return

        with open('money.json', 'r') as file:
                money = json.load(file)

        if int(amount) > money[str(ctx.guild.id)][str(ctx.author)]:
            await ctx.send('you dont have that much money pal...')

        elif int(amount) <= 0:
            await ctx.send('invalid amount')

        else:
            int_result = random.randint(0,3)
            result = money_collection.find_one({"guild": str(ctx.guild.id), "member": str(ctx.author)})

            if int_result == 0:
                money_collection.update_one({"guild": str(ctx.guild.id), "member": str(ctx.author)}, {"$set": {"money": result["money"]+int(amount)}})
                await ctx.send(f'Nice one! You won ${amount} \N{MONEY-MOUTH FACE}')

            else:
                money_collection.update_one({"guild": str(ctx.guild.id), "member": str(ctx.author)}, {"$set": {"money": result["money"]-int(amount)}})
                await ctx.send(f'RIP you lost ${amount} \N{GRIMACING FACE}')     

def setup(client):
    client.add_cog(Gambling_Commands(client))
