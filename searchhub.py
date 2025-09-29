import discord
from discord.ext import commands as selfCommands
from datetime import datetime
import requests
import asyncio
import json
import os
import mimetypes
import sys

self_bot = selfCommands.Bot(command_prefix="/", self_bot=True)

async def init_user(id):

    files = os.listdir("scrap/")

    if str(id) not in files:
        os.mkdir("scrap/"+str(id))
        os.mkdir(f"scrap/{id}/files")
        os.mkdir(f"scrap/{id}/user")

        messages_file = open(f"scrap/{id}/messages.json", "w")
        voice_file = open(f"scrap/{id}/voice.json", "w")
        messages_file.write('{}')
        voice_file.write('{}')
        messages_file.close()
        voice_file.close()

async def userinfo(id):
    user_folder = f"scrap/{id}/user"
    json_path = f"{user_folder}/userinfo.json"

    os.makedirs(os.path.dirname(json_path), exist_ok=True)

    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {
            "names": [],
            "pdp": []
        }

    def fetch_user_info():
        r = requests.get(f"https://discordlookup.mesalytic.moe/v1/user/{id}")
        if r.status_code == 200:
            return r.json()
        else:
            return False

    json_data = await asyncio.to_thread(fetch_user_info)
    if json_data:
        username = json_data.get("username", "")
        global_name = json_data.get("global_name", "")
        avatar_data = json_data.get("avatar", {})
        pdp = avatar_data.get("link", "")

        if not username and not global_name:
            return

        name_entry = f"{global_name} ( {username} )"

        if name_entry not in data["names"]:
            data["names"].append(name_entry)

        if pdp and pdp not in data["pdp"]:
            data["pdp"].append(pdp)
            response = requests.get(pdp)

            if response.status_code == 200:
                content_type = response.headers.get("Content-Type", "")
                extension = mimetypes.guess_extension(content_type)

                if extension is None:
                    extension = ".jpg"

                filename = f"scrap/{id}/user/{pdp.split('/')[5]}" + extension

                with open(filename, "wb") as f:
                    f.write(response.content)

                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)


@self_bot.event
async def on_disconnect():
    print("[WARNING] Déconnecté de Discord. Redémarrage...")
    python = sys.executable
    os.execv(python, [python] + sys.argv)  # Relance le script Python en entier

@self_bot.event
async def on_message(message):

    await init_user(message.author.id)
    await userinfo(message.author.id)
    
    if len(message.attachments) != 0:
        for attachment in message.attachments:
            try:
                await attachment.save(f"scrap/{message.author.id}/files/{attachment.filename}")
            except:
                pass
    
    if message.content != "":
        try:
            with open(f"scrap/{message.author.id}/messages.json", "r", encoding="utf-8") as file:
                json_content = json.load(file)

            if message.guild.name not in json_content:
                json_content[message.guild.name] = []

            json_content[message.guild.name].append(f"( {message.channel.name} ) - {message.content} ( {datetime.utcnow()} )")

            with open(f"scrap/{message.author.id}/messages.json", "w", encoding="utf-8") as file:
                json.dump(json_content, file, indent=4, ensure_ascii=False)
        except:
            pass

@self_bot.event
async def on_voice_state_update(member, before, after):
    
    await init_user(member.id)
    await userinfo(member.id)

    try:
        with open(f"scrap/{member.id}/voice.json", "r", encoding="utf-8") as file:
            json_content = json.load(file)
    except json.JSONDecodeError:
        json_content = {}
        with open(f"scrap/{member.id}/voice.json", "w", encoding="utf-8") as file:
            json.dump(json_content, file, indent=4, ensure_ascii=False)


    guild = None
    if before.channel and not after.channel:
        guild = before.channel.guild
    elif after.channel and not before.channel:
        guild = after.channel.guild
    elif after.channel and before.channel:
        guild = after.channel.guild
    else:
        return

    if guild.name not in json_content:
        json_content[guild.name] = []

    if before.channel == None and after.channel != None:
        json_content[guild.name].append(f"Connected to {after.channel.name} ( {datetime.utcnow()} )")
    
    if before.channel != None and after.channel == None:
        json_content[guild.name].append(f"Disconnected to {before.channel.name} ( {datetime.utcnow()} )")

    if before.channel != None and after.channel != None:
        if member.voice.self_mute and not member.voice.self_deaf:
            json_content[guild.name].append(f"Mute {after.channel.name} ( {datetime.utcnow()} )")
        elif member.voice.self_deaf:
            json_content[guild.name].append(f"Mute Casque {after.channel.name} ( {datetime.utcnow()} )")
        else:
            if before.channel == after.channel:
                json_content[guild.name].append(f"Unmute {after.channel.name} ( {datetime.utcnow()} )")
            else:
                json_content[guild.name].append(f"Moved to {after.channel.name} ( {datetime.utcnow()} )")

    with open(f"scrap/{member.id}/voice.json", "w", encoding="utf-8") as file:
        json.dump(json_content, file, indent=4, ensure_ascii=False)


@self_bot.event
async def on_ready():
    os.system('cls') if os.name == 'nt' else os.system('clear')
self_bot.run("")