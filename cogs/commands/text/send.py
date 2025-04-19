import discord
from discord.ext import commands
from json import load

from io import BytesIO

with open("config.json", 'r', encoding='utf-8') as file:
    config = load(file)


class send_command(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(name="send")
    @commands.has_guild_permissions(administrator=True)
    async def send(self, ctx: commands.Context, *, text: str):
        files = []
        for attachment in ctx.message.attachments:
            data = await attachment.read()
            fp = BytesIO(data)
            files.append(discord.File(fp, filename=attachment.filename))

        await ctx.message.delete()
        await ctx.message.channel.send(text, files=files)

    @send.error
    async def mute_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            msg = "❌ Fehlendes Argument: `!send <text>`."
        elif isinstance(error, commands.BadArgument):
            msg = "❌ Fehlerhafte Argumente."
        else:
            msg = "❌ Ein unbekannter Fehler ist aufgetreten."
            raise error
        await ctx.reply(msg, mention_author=False)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(send_command(client))