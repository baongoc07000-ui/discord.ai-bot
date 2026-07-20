import discord
from discord.ext import commands
import google.generativeai as genai
import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Online: {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user in message.mentions:
        try:
            user_msg = message.content.replace(f"<@{bot.user.id}>", "").strip()
            response = model.generate_content(user_msg)
            await message.reply(response.text)
        except Exception as e:
            await message.reply("Lỗi rồi 😢")

    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
