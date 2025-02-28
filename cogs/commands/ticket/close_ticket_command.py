import discord
from discord.ext import commands
from discord import app_commands
from json import load

from cogs.buttons.ticket_buttons import CloseConfirmButtons, color

with open("config.json", 'r', encoding='utf-8') as file:
    config = load(file)

class close_ticket_command(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
     
    @app_commands.command(name="close-ticket", description="Schließe dieses Ticket")
    @app_commands.guild_only()
    @app_commands.guilds(int(config["guild_id"]))
    @app_commands.default_permissions(manage_messages=True)
    async def close_ticket(self, interaction: discord.Interaction):
        channel = interaction.channel
        if str(channel.id) in self.client.ticket_list:
            embed = discord.Embed(description=f"## Ticket schließen\n\nMöchtest du wirklich dieses Ticket schließen? Klicke unten auf den roten Knopf, wenn du das Ticket schließen willst.", color=color["red"])
            embed.set_image(url=config["images"]["red_trash_line"])
            view = CloseConfirmButtons(self.client)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
            view.message = await interaction.original_response()
        else:
            await interaction.response.send_message("❌ Du bist nicht in einem Ticket", ephemeral=True)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(close_ticket_command(client))