from discord.ext import commands
from discord import app_commands
import json
import discord
import regex

class team_demote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="$", intents=intents)

    @app_commands.command(name="team-demote", description="Demote a member of a team")
    async def team_demote(self, interaction, team_name: str, member: str):
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
         
         def save_config(data):
            with open("config.json", "w") as f:
                json.dump(data, f, indent=4)

        ##########################################
        #                                        #
        #               Command:s                #
        #                                        #
        ##########################################
      
         config = load_config()
         guild_id = str(interaction.guild.id)
         server_roles = interaction.guild.roles

         regex_pattern = r"<@&(.*?)>"
         match = regex.match(regex_pattern, team_name)

         if match:
             team_name = match.group(1)
         else:
             await interaction.response.send_message("Invalid team name format. Please use the correct format and Ping the team role.")
             return


         regex_pattern = r"<@(.*?)>"
         match = regex.match(regex_pattern, member)

         if match:
            member = match.group(1)
         else:
            await interaction.response.send_message("Invalid member format. Please use the correct format and Ping the member/s.")
            return

         if not discord.utils.get(interaction.user.roles, name="Staff"):
            requester = interaction.user.id
            if config["guilds"][guild_id]["teams"][team_name]["member"][str(requester)]["leader"] != True:
                    await interaction.response.send_message(f"You have no permission to demote members.")
                    return


         if team_name not in config["guilds"][guild_id]["teams"]:
                await interaction.response.send_message(f"<@&{team_name}> is not registered.")
                return


         if member not in config["guilds"][guild_id]["teams"][team_name]["member"]:
                await interaction.response.send_message(f"<@{member}> is not a member of the team.")
                return
         
         if member == str(interaction.user.id):
                await interaction.response.send_message(f"You cannot demote yourself.")
                return

         if config["guilds"][guild_id]["teams"][team_name]["member"][member]["memberPlus"] == False:
                await interaction.response.send_message(f"<@{member}> cannot be demoted further.")
                return
         

         for role in server_roles:
            if role.id == int(team_name):

                    config["guilds"][guild_id]["teams"][team_name]["member"][member]["memberPlus"] = False
                    save_config(config)

                    await interaction.response.send_message(f"<@{member}> has been demoted.")
                    return

async def setup(bot):
    await bot.add_cog(team_demote(bot))
