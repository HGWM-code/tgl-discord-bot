from discord.ext import commands
from discord import app_commands
import json
import discord
import regex

class team_removeMember(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="$", intents=intents)

    @app_commands.command(name="team-remove-member", description="Remove a member from a team")
    async def team_removeMember(self, interaction, team_name: str, member: str):
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
         
         server_roles = interaction.guild.roles

         role_found = False
         for role in server_roles:
            if role.id == int(team_name):
               role_found = True

               config = load_config()
               guild_id = str(interaction.guild.id)

               member_alias = await interaction.guild.fetch_member(int(member))

               if team_name in config["guilds"][guild_id]["teams"]:
                     del config["guilds"][guild_id]["teams"][team_name]["member"][member]
                     save_config(config)

                     await interaction.response.send_message(f"<@{member}> has been removed from the team <@&{team_name}>.")
                     return
               else:
                     await interaction.response.send_message(f"<@&{team_name}> is not registered.")
                     break

async def setup(bot):
    await bot.add_cog(team_removeMember(bot))
