from discord.ext import commands
from discord import app_commands
import json
import discord

class counter_set(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="$", intents=intents)

    @app_commands.command(name="set_counter", description="Set the counter to a specific value")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_counter(self, interaction, count: str):
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
        
        guild = interaction.guild
        guild_id = str(guild.id)

        config["guilds"][guild_id]["count_to_100"] = int(count)
        save_config(config)
        await interaction.response.send_message(f"The counter was set to {count}")

async def setup(bot):
    await bot.add_cog(counter_set(bot))
