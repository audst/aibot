import discord
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('BOT_TOKEN')

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('!hello'):
            await message.channel.send('HIIII! ദ്ദി(˵ •̀ ᴗ - ˵ ) ✧')

        if message.content.startswith('!bye'):
            await message.channel.send('BYE (˶˃⤙˂˶)')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)