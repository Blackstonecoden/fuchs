import discord
from discord.ext import commands
from discord import app_commands
from json import load

from cogs.ui.voice_ui import VoiceButtons
from cogs.ui.ticket_ui import TicketMenuView

with open("config.json", 'r', encoding='utf-8') as file:
    config = load(file)


class setup_commands(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    setup_command = app_commands.Group(name="setup", description="Setup Befehl", default_permissions=discord.Permissions(administrator=True), guild_only=True)
    
    @setup_command.command(name="ticket", description="Erlaubt es dir die Ticket embed in diesem Kanal zu erstellen")
    async def setup_ticket(self, interaction: discord.Interaction):
        await interaction.response.send_message("✅ Ticket-Embed erfolgreich gesendet.", ephemeral=True)
        embed = discord.Embed(title=f"{config["emojis"]["mail"]} TICKET SUPPORT", description="> **Ticket Support Informationen**\n> - Die Wartezeit beträgt 0-48h\n > - Nutze die Tickets nur für Angebrachte Dinge. Die Fehlnutzung dieses Systems kann Folgen haben.\n\n> **Wie öffnet man ein Ticket?**\n > - Klicke auf das Menü unten und wähle die Kategorie aus, in die dein Ticket fällt, danach wird sich ein Ticketkanal für dich öffnen.\n> - Bitte habe etwas geduld, bis ein Teammitglied sich dort meldet.", color=0x6d6f78)
        embed.set_image(url=config["images"]["grey_ticket_line"])
        await interaction.channel.send(embed=embed, view=TicketMenuView(self.client))
 

    @setup_command.command(name="interface", description="Erlaubt es dir das Interface in diesem Kanal zu erstellen")
    async def setup_interface(self, interaction: discord.Interaction):
        channel = interaction.channel
        image = discord.File("images/card.png")
        embed = discord.Embed(title="Voice Interface", description="Mit diesem **Interface** kannst du deinen temporären Kanal bearbeiten.", color=0x6d6f78)    
        embed.set_image(url="attachment://card.png")
        await interaction.response.send_message("✅ Interface Embed erfolgreich gesendet.", ephemeral=True)
        await channel.send(embed=embed, files=[image], view=VoiceButtons(client=self.client))

async def setup(client:commands.Bot) -> None:
    await client.add_cog(setup_commands(client))