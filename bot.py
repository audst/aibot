import discord
import os
import random
from openai import AuthenticationError, OpenAI
from dotenv import load_dotenv

load_dotenv()
owner_id = int(os.getenv('OWNER_ID', 790688109229506601))
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

    async def help(self, message):
        if message.content.startswith('!help'):
            embed = discord.Embed(
                title = "୨ৎ welcome to ai bot ୨ৎ",
                description = (
                    "hi there! i am a bot that can answer ur questions~ (๑˃ᴗ˂)ﻭ\n\n"
                    "heres what i can do for u! 💖\n\n"
                    
                    "♡ `!ask <question>` — ask me anything! ⋆｡‧˚ʚ🍓ɞ˚‧｡⋆\n"
                    "♡ `!bye` — i miss u already!\n"
                    "♡ `!hello` — say hi to me!\n"
                    "♡ `!help` — see this message again!\n"
                    "♡ `!spinthewheel <list of things>` — spin the wheel and get a random item!\n\n"

                    "♡ more commands coming soon... (ฅ'ω'ฅ)"
                ),
                color = 0xffc0cb
            )
            embed.set_footer(text=" ૮₍ ´• ˕ •` ₎ა", icon_url="https://emojicombos.com/wp-content/uploads/2022/10/cute-star.png")
            await message.channel.send(embed = embed)

    async def hello(self, message):
        if message.content.startswith('!hello'):
            embed = discord.Embed(
                title = "୨୧ hello there! ୨୧",
                description = "i’m so happy to see u! ദ്ദി(˵ •̀ ᴗ - ˵ ) ✧",
                color = 0xffc0cb
            )
            await message.channel.send(embed = embed)

    async def bye(self, message):
        if message.content.startswith('!bye'):
            if (message.author.id == owner_id):
                embed = discord.Embed(
                    title = "୨୧ goodbye owner! ୨୧",
                    description = "miss u already! (˶˃⤙˂˶)",
                    color = 0xffc0cb
                )
                await message.channel.send(embed = embed)
                await self.close()
            else:
                embed = discord.Embed(
                    title = "୨୧ goodbye! ୨୧",
                    description = "i’ll be here when u come back! (๑˃ᴗ˂)ﻭ",
                    color = 0xffc0cb
                )
                await message.channel.send(embed = embed)

    async def spinthewheel(self, message):
        if message.content.startswith('!spinthewheel'):
            items = message.content[len('!spinthewheel '):].strip()
            if not items:
                embed = discord.Embed(
                    title = "୨୧ nothing to spin :/ ୨୧",
                    description = "please provide a list of items separated by commas! (,,>﹏<,,)˚",
                    color = 0xffc0cb
                )
                await message.channel.send(embed = embed)
                return
        
            items = [item.strip() for item in items.split(',')]
            items = [item for item in items if item]

            if not items:
                embed = discord.Embed(
                    title = "୨୧ looks like your list is empty ୨୧",
                    description = "please provide a list of items separated by commas! ⋆˚࿔",
                    color = 0xffc0cb
                )
                await message.channel.send(embed = embed)
                return
            
            if len(items) == 1:
                embed = discord.Embed(
                    title = "୨୧ only one item? ୨୧",
                    description = "i can’t spin a wheel with just one item! (๑•́ ₃ •̀๑)‧º·˚",
                    color = 0xffc0cb
                )
                await message.channel.send(embed = embed)
                return
            
            chosen_item = random.choice(items)
            embed = discord.Embed(
                title = "୨୧ spinning the wheel... ୨୧",
                description = f"the wheel landed on: **{chosen_item}**! (๑˃ᴗ˂)ﻭ",
                color = 0xffc0cb
            )
            await message.channel.send(embed = embed)

    async def ask(self, message):
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

    async def on_message(self, message):

        if message.author == self.user:
            return

        await self.ask(message)
        await self.bye(message)
        await self.hello(message)
        await self.help(message)
        await self.spinthewheel(message)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(bot_token)