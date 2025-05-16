from discord.ext import commands
from discord import app_commands
import json
import discord
import regex

class team_addMember(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="$", intents=intents)

    @app_commands.command(name="team-add-member", description="Add a member to a team")
    async def team_addMember(self, interaction, team_name: str, member: str):
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

               if not discord.utils.get(interaction.user.roles, name="Staff"):
                  requester = interaction.user.id
                  if config["guilds"][guild_id]["teams"][team_name]["member"][str(requester)]["leader"] != True:
                     await interaction.response.send_message(f"You you have no permissions to add members.")
                     return

               if team_name not in config["guilds"][guild_id]["teams"]:
                  await interaction.response.send_message(f"<@&{team_name}> is not registered.")
                  return  
               
               config["guilds"][guild_id]["teams"][team_name]["member"][member] = {"alias": member_alias.display_name, "leader": False, "memberPlus": False}
               save_config(config)

               for user in config["guilds"][guild_id]["teams"][team_name]["member"]:
                  if config["guilds"][guild_id]["teams"][team_name]["member"][user]["leader"] == True:
                     team_owner = user
                     break
               
               team_role = interaction.guild.get_role(int(team_name)) or discord.Color.default()

               embed = discord.Embed(title="New Member Added",
                     description=f"<@{member}> has been added to <@&{team_name}>.\n\nTeam Owner: <@{team_owner}>",
                     colour=(team_role.colour.r, team_role.colour.g, team_role.colour.b))
               embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url)
                     
               embed.set_thumbnail(url=interaction.guild.icon.url)

               await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(team_addMember(bot))
