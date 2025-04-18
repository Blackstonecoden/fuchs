import discord
from discord.ext import commands
from json import load

from io import BytesIO

with open("config.json", 'r', encoding='utf-8') as file:
    config = load(file)


class edit_command(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(name="edit")
    @commands.has_guild_permissions(administrator=True)
    async def edit(self, ctx: commands.Context, *, text: str):
        reference = await ctx.fetch_message(ctx.message.reference.message_id)
        if reference.author.id != self.client.user.id:
            return await ctx.reply("❌ Diese Nachricht wurde nicht vom Fuchs-Bot gesendet.", mention_author=False)
        
        files = []
        for attachment in ctx.message.attachments:
            data = await attachment.read()
            fp = BytesIO(data)
            files.append(discord.File(fp, filename=attachment.filename))

        await ctx.message.delete()
        await reference.edit(content=text, attachments=files)

    @edit.error
    async def mute_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            msg = "❌ Du hast nicht die ausreichenden Berechtigungen, um diesen Befehl verwenden zu können."
        elif isinstance(error, commands.MissingRequiredArgument):
            msg = "❌ Fehlendes Argument: `!edit <text>`."
        elif isinstance(error, commands.BadArgument):
            msg = "❌ Fehlerhafte Argumente."
        else:
            msg = "❌ Ein unbekannter Fehler ist aufgetreten."
            raise error
        await ctx.reply(msg, mention_author=False)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(edit_command(client))