import discord
import os
from openai import AuthenticationError, OpenAI
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv('BOT_TOKEN')
openai_api_key = os.getenv('OPENAI_API_KEY')

if not openai_api_key:
    print("error: OPENAI_API_KEY is not set in the environment variables.")
    exit(1)

try:
    openai_client = OpenAI(api_key=openai_api_key)
    print("openai client initialized successfully.")
except AuthenticationError:
    print("error: invalid api key")
    exit(1)
except Exception as e:
    print(f"error initializing openai client: {str(e)}")
    exit(1)

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

        if message.content.startswith('!ask'):
            question = message.content[len('!ask '):].strip()
            if not question:
                await message.channel.send('please ask a question after !ask')
                return
            
            await message.channel.send('thinking...')
            try:
                response = openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "you are a kind and polite assistant."
                        },
                        {
                            "role": "user",
                            "content": question
                        }
                    ],
                    max_tokens=100,
                )
                await message.channel.send(response.choices[0].message.content)
            except Exception as e:
                await message.channel.send(f'error!!: {str(e)}')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(bot_token)