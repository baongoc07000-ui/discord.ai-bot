import discord
from discord.ext import commands
import google.generativeai as genai
import os

# ====== ENV ======
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

print("TOKEN:", DISCORD_TOKEN)
print("GEMINI:", GEMINI_API_KEY)

# ====== CHECK ENV ======
if not DISCORD_TOKEN:
    raise ValueError("❌ Thiếu DISCORD_TOKEN")

if not GEMINI_API_KEY:
    raise ValueError("❌ Thiếu GEMINI_API_KEY")

# ====== GEMINI ======
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ====== DISCORD ======
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ====== READY ======
@bot.event
async def on_ready():
    print(f"🟢 Online: {bot.user}")

# ====== MESSAGE ======
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Khi tag bot
    if bot.user in message.mentions:
        try:
            user_msg = message.content.replace(f"<@{bot.user.id}>", "").strip()

            if not user_msg:
                await message.reply("Bạn chưa hỏi gì 😅")
                return

            response = model.generate_content(user_msg)

            if response and hasattr(response, "text") and response.text:
                await message.reply(response.text)
            else:
                await message.reply("Không có phản hồi 😢")

        except Exception as e:
            print("❌ ERROR:", e)
            await message.reply("Bot bị lỗi 😢")

    await bot.process_commands(message)

# ====== RUN ======
bot.run(DISCORD_TOKEN)
