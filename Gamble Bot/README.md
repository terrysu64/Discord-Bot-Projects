<h1>The Gamble Bot 💰</h1>

<h3>Tech Stack</h3>
<div>
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
<img src="https://img.shields.io/badge/Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white" alt="Discord">
 </div>
 
### Setup
1. Install Project and Dependencies
```bash
$ git clone https://github.com/terrysu64/Discord-Bot-Projects.git
$ cd ./Gamble Bot
$ pip3 install discord pymongo dotenv
```
2. Seteup Your Own MongoDB Cluster
3. Create a `.env` With Personal Environment Variables
4. Import Into `main.py` and Begin Developing!
```Python
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
import os
from pymongo import MongoClient

#INITIALIZING 

bot_token = os.environ.get("BOT_TOKEN")
bot_maintenance_channel_id = os.environ.get("MAINTENANCE_CHANNEL")
database_password = os.environ.get("DATABASE_PASSWORD")

cluster = MongoClient(f'{your database}')
db = cluster["gamble-bot"]
prefixes_collection = db["prefixes"]
money_collection = db["money"]
```

<h3>Usage and Commands</h3>

<h3>Issues and Updates</h3>

- usage
  - commands
  Gambling_Commands:
  borrow        
  flip_coin     
  raw_bet       
  roll_dice     
General_Commands:
  change_prefix 
  info          
  ping          
Money_Commands:
  leaderboard   
  rich          
​No Category:
  help          Shows this message

- issues and updates
