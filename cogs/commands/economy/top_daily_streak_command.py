import discord
from discord.ext import commands
from discord import app_commands
from json import load

from database.models import EconomyUser

with open("config.json", 'r', encoding='utf-8') as file:
    config = load(file)


class top_daily_streak_command(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="top-daily-streak", description="Zeigt dir die Nutzer mit den höchsten täglichen Serien an")
    @app_commands.guild_only()
    @app_commands.guilds(int(config["guild_id"]))
    async def top_daily_streak(self, interaction: discord.Interaction):
        await interaction.response.defer()
        economy_user = await EconomyUser(interaction.user.id).load()
        top_raw = await economy_user.get_top_users("daily_streak")

        user_list = ""
        pos = 1  
        for u in top_raw:
            user: discord.User = self.client.get_user(u[0])
            if user:
                if u[2] > 1 or u[2] == 0:
                    user_list += f"**#{pos}** • {user.name} • {u[2]} Tage\n"
                else:
                    user_list += f"**#{pos}** • {user.name} • {u[2]} Tag\n"
            else:
                user_list += f"**#{pos}** • `Null` • `Null` Tage\n"
            pos += 1
        embed = discord.Embed(title="Top tägliche Serien", description=user_list, color=0xa7acb4)
        embed.set_thumbnail(url=interaction.guild.icon.url)
        await interaction.edit_original_response(embed=embed)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(top_daily_streak_command(client))