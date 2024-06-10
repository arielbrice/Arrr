# bot.py
import os

import discord
import pydest
from dotenv import load_dotenv
from discord import app_commands

load_dotenv()
TOKEN = os.getenv('TOKEN')
BUNGIE_TOKEN = os.getenv('BUNGIE_TOKEN')
platforms = {'XBOX': 1, 'PLAYSTATION': 2, 'PC': 3}

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

@client.tree.command()
async def destiny(interaction: discord.Interaction):

    destiny = pydest.Pydest(BUNGIE_TOKEN)
    activity1 = await destiny.decode_hash(18699611, 'DestinyActivityDefinition')
    await destiny.update_manifest()
    activity2 = await destiny.decode_hash(80726883, 'DestinyActivityDefinition')

    print("Activity Name: {}".format(activity1['displayProperties']['name']))
    print("Description: {}".format(activity1['displayProperties']['description']))
    print("")
    print("Activity Name: {}".format(activity2['displayProperties']['name']))
    print("Description: {}".format(activity2['displayProperties']['description']))

    await destiny.close()


@client.tree.command()
async def finddestinyuser(interaction: discord.Interaction):
    destiny = pydest.Pydest(BUNGIE_TOKEN)

    platform = None
    while not platform:
        user_input = input('Enter your platform (xbox, playstation, or pc): ')
        if user_input.upper() in platforms.keys():
            platform = platforms.get(user_input.upper())
        else:
            print('Invalid platform.')

    username = input('Enter the username to locate: ')
    res = await destiny.api.search_destiny_player(platform, username)

    if res['ErrorCode'] == 1 and len(res['Response']) > 0:
        print("---")
        print("Player found!")
        print("Display Name: {}".format(res['Response'][0]['displayName']))
        print("Membership ID: {}".format(res['Response'][0]['membershipId']))
        print(res['Response'])
    else:
        print("Could not locate player.")

    await destiny.close()


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