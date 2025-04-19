import os
from dotenv import load_dotenv
import json
from pathlib import Path
import warnings
from logging import WARN

import discord
from discord.ext import commands
from discord import app_commands

import time
from colorama import Fore, Back, Style
import platform

from cogs.ui.ticket_ui import TicketMenuView, TicketButtons, DeleteTicketButtons
from cogs.ui.voice_ui import VoiceButtons

from aiomysql import Pool
from aiomysql import Warning as MySQLWarning 
from database.models import get_pool
import aiofiles
import asyncio

load_dotenv()
with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)
with open("json/data.json", "r", encoding="utf-8") as file:
    storage = json.load(file)


if not os.path.exists("json"):
    os.makedirs("json")
if not os.path.exists("json/data.json"):
    with open("json/data.json", "w", encoding="utf-8") as file:
        json.dump({"community_server_status": "False","counting_current_number": 2,"counting_last_user": 1204122491929366558}, file, ensure_ascii=False, indent=4)
if not os.path.exists("json/tickets.json"):
    with open("json/tickets.json", "w", encoding="utf-8") as file:
        json.dump({}, file, ensure_ascii=False, indent=4)

async def on_tree_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        if error.retry_after >= 60:
            if interaction.command.name == "work":
                await interaction.response.send_message(content=f"⌛ Du arbeitest bereits. Warte **{round(error.retry_after/60)}** Minuten um deine Belohnung abzuholen.", ephemeral=True)   
            else:
                await interaction.response.send_message(content=f"⌛ Bite warte **{round(error.retry_after/60)}** Minuten, bevor du diesen Befehl noch einmal verwenden kannst.", ephemeral=True)
        else:
            if interaction.command.name == "work":
                await interaction.response.send_message(content=f"⌛ Du arbeitest bereits. Warte **{round(error.retry_after)}** Sekunden um deine Belohnung abzuholen.", ephemeral=True)
            else:                
                await interaction.response.send_message(content=f"⌛ Bite warte **{round(error.retry_after)}** Sekunden, bevor du diesen Befehl noch einmal verwenden kannst.", ephemeral=True)

async def init_db():
    pool: Pool = await get_pool()
    async with aiofiles.open("database/structure.sql") as file:
        sql = await file.read()
    async with pool.acquire() as connection:
        async with connection.cursor() as cursor:
            for statement in sql.split(";"):
                try:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore", MySQLWarning) 
                        await cursor.execute(statement)
                except Exception as e:
                    print(e)
    pool.close()
    await pool.wait_closed()

class Client(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)

        asyncio.run(init_db())
        self.tree.on_error = on_tree_error
        self.cogslist = [".".join(file.relative_to("cogs").with_suffix("").parts) for file in Path("cogs").rglob("*.py") if not file.name.startswith("__")]
        self.storage = storage


    async def setup_hook(self):
        for cog in self.cogslist:
            await self.load_extension("cogs."+cog)

    async def on_ready(self):
        self.add_view(VoiceButtons(client))
        self.add_view(TicketMenuView(client))
        self.add_view(TicketButtons(client))
        self.add_view(DeleteTicketButtons(client))

        os.system("cls" if os.name == "nt" else "clear")
        prfx = (Back.BLACK + Fore.CYAN + time.strftime("%H:%M:%S", time.gmtime()) + Back.RESET + Fore.WHITE + Style.NORMAL)
        print(prfx + " Logged in as " + Fore.BLUE + self.user.name)
        print(prfx + " Bot ID " + Fore.BLUE + str(self.user.id))
        print(prfx + " Discord Version " + Fore.BLUE+ discord.__version__)
        print(prfx + " Python Version " + Fore.BLUE + str(platform.python_version()))
        print (prfx + " Cogs Loaded " + Fore.BLUE + str(len(self.cogslist)))
        await self.tree.sync()
        synced = await self.tree.sync(guild=discord.Object(id=config["guild_id"]))
        print(prfx + " Slash CMDs Synced " + Fore.BLUE + str(len(synced)) + " Commands")
        print("")
        await client.change_presence(activity = discord.CustomActivity(name=config["custom_app_status"]))

if __name__ == "__main__":
    client = Client()
    client.remove_command("help")
    client.run(os.getenv("TOKEN"), log_level=WARN)