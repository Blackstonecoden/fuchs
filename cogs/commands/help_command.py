import discord
from discord.ext import commands
from discord import app_commands
from json import load

with open("config.json", 'r', encoding='utf-8') as file:
    config = load(file)

class help_command(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="help", description="Zeigt dir eine kleine Hilfestellung")
    @app_commands.guild_only()
    @app_commands.guilds(int(config["guild_id"]))
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"{config["emoji"]["file_text"]} HILFESTELLUNG", description="> **Level System**\n> - `/level` - Zeigt dir dein Level und andere Informationen an\n> - `/level-leaderboard` - Zeigt die Nutzer mit den höchsten Leveln an\n\n> **Economy System**\n> - `/balance` - Zeigt dir deinen Kontostand an\n> - `/daily` - Bekomme deine tägliche Belohnung\n> - `/work` - Arbeite für etwas Geld\n> - `/balance-top` - Zeigt die Nutzer mit dem höchsten Kontostand an\n> - `/top-daily-streak` Zeigt die Nutzer mit den höchsten täglichen Serien an", color=0x6d6f78)
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(help_command(client))