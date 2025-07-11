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
        
        if message.content.startswith('!help'):
            embed = discord.Embed(
                title = "୨ৎ welcome to ai bot ୨ৎ",
                description = (
                    "hi there! i am a bot that can answer ur questions~ (๑˃ᴗ˂)ﻭ\n"
                    "heres what i can do for u! 💖\n\n"
                    "♡ `!hello` — say hi to me!\n"
                    "♡ `!bye` — i miss u already~\n"
                    "♡`!ask <question>` — ask me anything and i will think really hard about it! ⋆｡‧˚ʚ🍓ɞ˚‧｡⋆\n"
                    "♡ more commands coming soon... (ฅ'ω'ฅ)"
                ),
                color = 0xffc0cb
            )
            embed.set_footer(text=" ૮₍ ´• ˕ •` ₎ა", icon_url="https://emojicombos.com/wp-content/uploads/2022/10/cute-star.png")
            await message.channel.send(embed = embed)

        if message.content.startswith('!hello'):
            embed = discord.Embed(
                title = "୨୧ hello there! ୨୧",
                description = "i’m so happy to see u! ദ്ദി(˵ •̀ ᴗ - ˵ ) ✧",
                color = 0xffc0cb
            )
            await message.channel.send(embed = embed)

        if message.content.startswith('!bye'):
            embed = discord.Embed(
                title = "୨୧ goodbye! ୨୧",
                description = "miss u already! (˶˃⤙˂˶)",
                color = 0xffc0cb
            )
            await message.channel.send(embed = embed)

        if message.content.startswith('!ask'):
            question = message.content[len('!ask '):].strip()
            if not question:
                embed = discord.Embed(
                    title = "୨୧ ask me something! ୨୧",
                    description = "i can’t answer nothing! (๑•́ ₃ •̀๑)‧º·˚",
                    color = 0xffc0cb
                )
                await message.channel.send(embed = embed)
                return
            
            await message.channel.send('thinking... ₍ᐢ. .ᐢ₎ ₊˚⊹♡')
            try:
                response = openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "you are a cute and friendly assistant that uses all lowercase letters and emojis in your responses. you are very helpful and always try to be positive and encouraging. you love to use cute expressions and kaomoji in your replies",
                        },
                        {
                            "role": "user",
                            "content": question
                        }
                    ],
                    max_tokens=100,
                )

                embed = discord.Embed(
                    title = "୨୧ here’s what i think! ୨୧",
                    description = response.choices[0].message.content.strip(),
                    color = 0xffc0cb
                )
                await message.channel.send(embed = embed)
            except Exception as e:
                embed = discord.Embed(
                    title = "୨୧ oops! ୨୧",
                    description = f"i’m having trouble answering that... (｡•́︿•̀｡)\nerror: {str(e)}",
                    color = 0xffc0cb
                )
                await message.channel.send(embed = embed)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(bot_token)