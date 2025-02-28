import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
from json import load

from database.models import EconomyUser

with open("config.json", 'r', encoding='utf-8') as file:
    config = load(file)

class daily_command(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="daily", description="Bekomme deine täglichen Belohnung")
    @app_commands.guild_only()
    @app_commands.guilds(int(config["guild_id"]))
    async def daily(self, interaction: discord.Interaction):
        economy_user = await EconomyUser(interaction.user.id).load()
        if economy_user.last_daily.date() != datetime.now().date():
            last_daily = datetime.strptime(str(datetime.now().replace(microsecond=0)), '%Y-%m-%d %H:%M:%S')
            if economy_user.last_daily.date() != (datetime.now() - timedelta(days=1)).date():
                coins = int(config["daily_rewards"]["0"]*economy_user.multiplier)
                daily_streak = 1
            else:
                coins = int(config["daily_rewards"][str(min(economy_user.daily_streak, len(config["daily_rewards"])-1))]*economy_user.multiplier)
                daily_streak = economy_user.daily_streak + 1
                
            await economy_user.add_data(coins=coins,last_daily=last_daily,daily_streak=daily_streak)
            await interaction.response.send_message(f"✅ Du hast erfolgreich deine tägliche Belohnung gesammelt und {coins} 🪙 erhalten. Deine tägliche Serie liegt jetzt bei {daily_streak}/7.")
        else:
            await interaction.response.send_message("⌛ Du kannst erst morgen wieder deine tägliche Belohnung einsammeln.", ephemeral=True)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(daily_command(client))