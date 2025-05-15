import os
import json
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)


##########################################
#                                        #
#             load Config                #
#                                        #
##########################################


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
#               onReady                  #
#                                        #
##########################################

@bot.event
async def on_ready(): # Wenn der Bot Startet werden folgende Sachen überprüft

    await bot.tree.sync() # synced alle application commands vom bot
    print(f'Bot ist eingeloggt als {bot.user}')

    config = load_config()

    active_guilds = {str(guild.id) for guild in bot.guilds}

    # Entfernt Server aus der JSON, auf denen der Bot nicht mehr ist
    removed_guilds = [gid for gid in config["guilds"] if gid not in active_guilds]
    for guild_id in removed_guilds:
        del config["guilds"][guild_id]
        print(f'Removed old guild from config: {guild_id}')

    # Falls neue Server fehlen, hinzufügen in die Json
    for guild in bot.guilds:
        guild_id = str(guild.id)
        if guild_id not in config["guilds"]:
            config["guilds"][guild_id] = {"teams": {}}
            print(f'Added new guild to config: {guild.name} (ID: {guild.id})')
        else:
            if "teams" not in config["guilds"][guild_id]:
                config["guilds"][guild_id]["teams"] = {}
                print(f"Added missing key 'teams' for guild {guild.name} (ID: {guild.id})")
        
    save_config(config)


@bot.event
async def on_guild_join(guild):    #Wenn der Bot einen Server joint
    
    config = load_config()
    guild_id = str(guild.id)

    if guild_id not in config["guilds"]:
        config["guilds"][guild_id] = {"team": {}}
        save_config(config)
        print(f'New guild added: {guild.name} (ID: {guild.id})')    #Wenn der Bot einem neuen Server beitritt wird er zur JSON hinzugefügt

@bot.event
async def on_guild_remove(guild):     #Wenn der Bot einen Server verlässt

    config = load_config()
    guild_id = str(guild.id)

    if guild_id in config["guilds"]:
        del config["guilds"][guild_id]
        save_config(config)
        print(f'Guild removed: {guild.name} (ID: {guild.id})')  #Wenn der Bot einem Server verlässt wird er von der JSON entfernt


@bot.event
async def on_message(message): 

    if message.author.bot:
        return
    
    #Empty for now
    
    await bot.process_commands(message)


async def load_extensions():    # laden der Commands
    await bot.load_extension("commands.greeting") 
    await bot.load_extension("commands.message_clear") 
    await bot.load_extension("commands.team_register") 
    await bot.load_extension("commands.team_unregister")
    await bot.load_extension("commands.team_addMember")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

import asyncio
asyncio.run(main())