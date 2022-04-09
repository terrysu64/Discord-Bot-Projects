from unicodedata import name
import discord 
from discord.ext import commands
import os
import uuid
import requests
import shutil
from imageai.Prediction import ImagePrediction

execution_path = os.getcwd() 

prediction = ImagePrediction()

prediction.setModelTypeAsMobileNetV2() 
prediction.setModelPath(os.path.join(execution_path, 'mobilenet_v2.h5'))
prediction.loadModel()

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = '+' , intents = intents)

bot_token = 'OTYyMTI1MTAxNTUyMjYzMjA5.YlC-0w.Wzq9Zpf0weSxnhFvIgLhOYOIeGI'
bot_maintenance_channel_id = 858869667865821194

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.get_channel(bot_maintenance_channel_id).send("GoodEye Bot is updated and ready to go!") 

#MAIN FUNCTIONS
@client.command()
async def identify(ctx):

    try:
        url = ctx.message.attachments[0].url         
    except IndexError:
        print("Error: No Image")
        await ctx.send("You didn't send a valid image LOL")
    else:
        if url[0:26] == "https://cdn.discordapp.com":   
            r = requests.get(url, stream=True)
            imageName = str(uuid.uuid4()) + '.jpg'     
            with open(imageName, 'wb') as out_file:
                print(f'Image Saved: {imageName}')
                shutil.copyfileobj(r.raw, out_file)
                
        await ctx.send('How many possibilities would you like me to tell you? Please enter a positive number.')

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        try:
            possi = await client.wait_for('message', check=check)

            predictions, probabilities = prediction.classifyImage(os.path.join(execution_path, imageName), result_count = int(possi.content) ) 
            cnt=1
            embed = discord.Embed(title = 'Hmm. Here are my guesses 🧠:')
            for eachPrediction, eachProbability in zip(predictions, probabilities):
                eachPrediction = ' '.join([prediction.lower() for prediction in eachPrediction.split('_')])
                eachProbability = str(round(float(eachProbability), 2))
                if cnt==1: embed.add_field(name = f'{eachPrediction} \N{FIRST PLACE MEDAL}', value=f'{eachProbability}%')
                elif cnt==2: embed.add_field(name = f'{eachPrediction} \N{SECOND PLACE MEDAL}', value=f'{eachProbability}%')
                elif cnt==3: embed.add_field(name = f'{eachPrediction} \N{THIRD PLACE MEDAL}', value=f'{eachProbability}%')
                else: embed.add_field(name = f'{eachPrediction}', value=f'{eachProbability}%')
                cnt+=1
            await ctx.send(embed = embed)

        except:
             await ctx.send('An error has occured. Please check that all your inputs were valid.')

@client.command()
async def colorize(ctx):

    try:
        url = ctx.message.attachments[0].url         
    except IndexError:
        print("Error: No Image")
        await ctx.send("You didn't send a valid image LOL")
    else:
        if url[0:26] == "https://cdn.discordapp.com":   
            r = requests.get(url, stream=True)
            imageName = str(uuid.uuid4()) + '.jpg'     
            with open(imageName, 'wb') as out_file:
                print(f'Image Saved: {imageName}')
                shutil.copyfileobj(r.raw, out_file)
                
        res = requests.post(
            "https://api.deepai.org/api/colorizer",
            files={
                'image': open(imageName, 'rb'),
            },
            headers={'api-key': 'c0a71c7f-f930-4864-9546-899358953d11'}
        )
        print(res.json())
        await ctx.send(res.json()['output_url'])

@client.command()
async def deepdream(ctx):
    try:
        url = ctx.message.attachments[0].url         
    except IndexError:
        print("Error: No Image")
        await ctx.send("You didn't send a valid image LOL")
    else:
        if url[0:26] == "https://cdn.discordapp.com":   
            r = requests.get(url, stream=True)
            imageName = str(uuid.uuid4()) + '.jpg'     
            with open(imageName, 'wb') as out_file:
                print(f'Image Saved: {imageName}')
                shutil.copyfileobj(r.raw, out_file)
                

        res = requests.post(
            "https://api.deepai.org/api/deepdream",
            files={
                'image': open(imageName, 'rb'),
            },
            headers={'api-key': 'c0a71c7f-f930-4864-9546-899358953d11'}
        )
        print(res.json())
        await ctx.send(res.json()['output_url'])

@client.command()
async def generate(ctx):
    try:
        msg = ctx.message.content.split()[1]
        res = requests.post(
            "https://api.deepai.org/api/text2img",
            data={
                'text': msg,
            },
            headers={'api-key': 'c0a71c7f-f930-4864-9546-899358953d11'}
        )
        print(res.json())
        await ctx.send(res.json()['output_url'])
    except:
        await ctx.send('An error has occured. Please check that all your inputs were valid.')
        
    
#EXTRA
@client.command()
async def ping(ctx): 
    await ctx.send(f'Pong 🏓')
    await ctx.send(f'Your internet latency is {round(client.latency * 1000)}ms')

client.run(bot_token)
