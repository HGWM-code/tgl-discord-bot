from discord.ext import commands
from discord import app_commands
import json
import discord

class counter_setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ##########################################
    #                                        #
    #               Commands                #
    #                                        #
    ##########################################

    @app_commands.command(name="setup_counter", description="Setup a Counter Channel")
    async def setup_counter(self, interaction):

        guild = interaction.guild
        guild_id = str(guild.id)

        channel = discord.utils.get(guild.channels, name='count-to-100')
        if not channel:
            await guild.create_text_channel('count-to-100')
            await interaction.response.send_message("Created the Counter Channel")
        else:
             await interaction.response.send_message("The Counter Channel already exist.")

async def setup(bot):
    await bot.add_cog(counter_setup(bot))
