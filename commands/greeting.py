from discord.ext import commands
from discord import app_commands
import json
import discord

class greeting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="$", intents=intents)

    @app_commands.command(name="greeting", description="Say hello!")
    async def greeting(self, interaction):
        #############################################################
        #                                                           #
        #   Common setup for each Command interacting with Config   #
        #                                                           #
        #############################################################

        def load_config():
            try:
                with open("config.json", "r") as f:
                    return json.load(f)
            except FileNotFoundError:
                    return {"guilds": {}}    # Wenns die Config Datei nicht vorhanden ist wird eine Leere Config Liste erstellt

        config = load_config()

        def save_config(data):
            with open("config.json", "w") as f:
                json.dump(data, f, indent=4)

        ##########################################
        #                                        #
        #               Command:s                #
        #                                        #
        ##########################################

        await interaction.response.send_message("hello")

async def setup(bot):
    await bot.add_cog(greeting(bot))
