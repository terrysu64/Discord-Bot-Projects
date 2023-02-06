<h1>The Gamble Bot 💰</h1>

<h3>Tech Stack</h3>
<div>
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
<img src="https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white" alt="mongo">
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

`$borrow`: plays secret game with users with zero or negative earnings for a chance to gain a $5 starter pack

`$flip_coin`: 1/2 chance of +- $10

`$raw_bet`: 1/4 chance of losing or doubling a sum of the user's choice

`$roll_dice`: 1/6 chance of +- $60

`$change_prefix`: change command prefix for bot

`$info $help`: general info/help section about the bot

`$ping`: connection latency check (in ms)

`$leaderboard`: displays guild leaderboard (sorted by net worth in descending order)

`$rich`: lets user check their current net worth

<h3>Issues and Updates</h3>

- Feel free to create PRs and raise relevant issues in the repo!
- New feature under construction: `mini-games mode 🎱`
- Playing around with Web3 and Solidity smart contracts (may incorporate real-time betting on the Goreli network)
  

