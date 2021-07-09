#Date: June 29, 2021
#Author: Terry Su
#Purpose: a cog for Terry's Test Bot.py that concerns vc related commands (not working)

import discord
from discord.ext import commands
import youtube_dl

class Music_Commands(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_ready(self):
        print("Terry's Test Bot - Music Commands has been loaded!")
    

    @commands.command()
    async def join(self,ctx):

        if ctx.author.voice is None:
            await ctx.send('not in vc')

        voice_channel = ctx.author.voice.channel

        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)


    @commands.command()
    async def disconnect(self,ctx):
        await ctx.voice_client.disconnect()


    @commands.command()
    async def play(self,ctx,url):

        ctx.voice_client.stop()
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 - reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPTIONS = {'format': "bestaudio"}
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download = False)
            url2 = info['format'][0]['url']
            source = await discord.FFmpeg0pusAudio.from_probe(url2,**FFMPEG_OPTIONS)
            vc.play(source)
    
    

def setup(client):
    client.add_cog(Music_Commands(client))
