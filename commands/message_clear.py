from discord.ext import commands
from discord import app_commands
from discord import app_commands, Interaction

class clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clear", description="clear the chat")
    @app_commands.describe(amount="amount of massages to delete (max. 100).")
    async def clear(self, interaction: Interaction, amount: int):

        await interaction.channel.purge(limit=amount)
        await interaction.response.send("Messages deleted")

async def setup(bot):
    await bot.add_cog(clear(bot))