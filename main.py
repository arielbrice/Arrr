# bot.py
import os

import discord
from dotenv import load_dotenv
from discord import app_commands

load_dotenv()
TOKEN = os.getenv('TOKEN')


client = discord.Client(intents=discord.Intents.default())
MY_GUILD = discord.Object(os.getenv('GUILD'))

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
    


intents = discord.Intents.default()
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')


client.run(TOKEN)

#TODO:
#Connect to twitch?
#Bungie Information?
## Raid Challenges
## Bungie Name
## Triumphs?
## Raid Completions
#Queue, linked to twitch chat
#Gambling