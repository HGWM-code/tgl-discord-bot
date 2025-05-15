from discord.ext import commands
from discord import app_commands
import json
import discord

class register_team(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="$", intents=intents)

    @app_commands.command(name="register-team", description="Register a Team for a scrim")
    async def register_team(self, interaction, user_id: str, team_name: str):

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

        config = load_config()
        guild = interaction.guild
        guild_id = str(guild.id)

        user = guild.get_member(int(user_id))

        teams = config["guilds"][guild_id]["teams"]
        if team_name in teams:
            await interaction.response.send_message(f"Team {team_name} is already registered.")

            role = discord.utils.get(guild.roles, name=team_name)

            await user.add_roles(role)
            await interaction.response.send_message(f"<&!{user}> has been added to {team_name}.")
        else: 
            teams[team_name] = {"members": [user]}
            save_config(config)

            await guild.create_role(name=team_name)

            role = discord.utils.get(guild.roles, name=team_name)
            user = guild.get_member(int(user_id))

            await user.add_roles(role)
            await interaction.response.send_message(f"<&!{user}> has been added to {team_name}.")

            await interaction.response.send_message(f"Team {team_name} has been registered successfully.")
        
        

async def setup(bot):
    await bot.add_cog(register_team(bot))