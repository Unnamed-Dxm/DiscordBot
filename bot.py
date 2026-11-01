import os
import aiohttp
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
N8N_URL = os.getenv("N8N_URL", "http://localhost:5678/webhook/mmm")
GUILD_ID = os.getenv("GUILD_ID")

client = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)

@tree.command(name="mmm", description="Best money making methods for your SkyBlock profile")
@app_commands.describe(username="Your Minecraft username", gear="Optional extra info about your gear")
async def mmm(interaction: discord.Interaction, username: str, gear: str = ""):
    await interaction.response.defer()
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(N8N_URL, params={"name": username, "gear": gear}, timeout=aiohttp.ClientTimeout(total=120)) as r:
                data = await r.json()
        await interaction.followup.send(data.get("advies", "No advice received.")[:2000])
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")

@client.event
async def on_ready():
    if GUILD_ID:
        guild = discord.Object(id=int(GUILD_ID))
        tree.copy_global_to(guild=guild)
        await tree.sync(guild=guild)
    else:
        await tree.sync()
    print(f"Logged in as {client.user}")

client.run(TOKEN)
