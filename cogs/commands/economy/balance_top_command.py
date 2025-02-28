import discord
from discord.ext import commands
from discord import app_commands
from json import load
import math
from database.models import EconomyUser

with open("config.json", 'r', encoding='utf-8') as file:
    config = load(file)

def convert(number: int) -> str:
    if number >= 10**9: 
        exponent = int(math.log10(number))
        mantissa = number / 10**exponent
        return f"{mantissa:.1f}E+{exponent}"
    elif number >= 10000:
        return f"{number // 1000}k"
    elif number >= 1000:
        return f"{(number / 1000):.1f}k"
    elif number < 0:
        return "∞"
    else:
        return str(number)

class balance_top_command(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="balance-top", description="Zeigt die 10 reichsten Mitglieder an")
    @app_commands.guild_only()
    @app_commands.guilds(int(config["guild_id"]))
    async def balance_top(self, interaction: discord.Interaction):
        await interaction.response.defer()
        economy_user = await EconomyUser(interaction.user.id).load()
        top_raw = await economy_user.get_top_users()
        
        user_list = ""
        pos = 1  
        for u in top_raw:
            user: discord.User = self.client.get_user(u[0])
            if user:
                coins = convert(u[1])

                user_list += f"**#{pos}** • {user.name} • {coins} 🪙\n"
            else:
                user_list += f"**#{pos}** • `Null` • None 🪙\n"
            pos += 1
        embed = discord.Embed(title="Top Coins", description=user_list, color=0xa7acb4)
        embed.set_thumbnail(url=interaction.guild.icon.url)
        await interaction.edit_original_response(embed=embed)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(balance_top_command(client))