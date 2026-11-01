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

@tree.command(name="mmm", description="Beste money making method voor jouw profiel")
@app_commands.describe(naam="Je Minecraft-naam", gear="Je belangrijkste gear")
async def mmm(interaction: discord.Interaction, naam: str, gear: str = ""):
    await interaction.response.defer()
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(N8N_URL, params={"name": naam, "gear": gear}, timeout=aiohttp.ClientTimeout(total=120)) as r:
                data = await r.json()
        await interaction.followup.send(data.get("advies", "Geen advies ontvangen.")[:2000])
    except Exception as e:
        await interaction.followup.send(f"Fout: {e}")

@client.event
async def on_ready():
    if GUILD_ID:
        guild = discord.Object(id=int(GUILD_ID))
        tree.copy_global_to(guild=guild)
        await tree.sync(guild=guild)
    else:
        await tree.sync()
    print(f"Ingelogd als {client.user}")

client.run(TOKEN)
client.run(TOKEN)
