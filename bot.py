import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.load_extension("cogs.verification")
    await bot.load_extension("cogs.setup")
    await bot.tree.sync()
    print(f"✅ Bot conectado como {bot.user} ({bot.user.id})")
    print(f"📡 En {len(bot.guilds)} servidor(es)")

bot.run(TOKEN)
