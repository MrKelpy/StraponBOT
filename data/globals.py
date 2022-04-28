# -*- coding: utf-8 -*-
"""
This file is distributed as part of the <project_name> Project.
The source code may be available at
https://github.com/MrKelpy/<project_name>

If a license applies for this project, the former can be found
in every distribution, as a "LICENSE" file at top level.
"""

# Built-in Imports
from typing import Dict
import json

# Third Party Imports
from discord.ext import commands as cmds
from discord import Intents
import discord

# Local Application Imports
from resources.config_handler.load_settings import load_settings
from resources.LaminariaCore.utils.discordpy import DPyUtils
from resources.LaminariaDB.LaminariaDB import LaminariaDB

settings: Dict[str, str] = load_settings("./data/bot.config")
token: str = settings["token"]
prefix: str = settings["prefix"]
intents = Intents.default()
intents.members = True
bot: cmds.Bot = cmds.Bot(command_prefix=prefix, intents=intents)
dpyutils: DPyUtils = DPyUtils()
MUDAE_ID: int = 432610292342587392
FAILED_EMOJI: str = "❌"
SUCCESS_EMOJI: str = "✅"
NEXT_EMOJI: str = "➡"
PREV_EMOJI: str = "⬅"
waifus_db: LaminariaDB = LaminariaDB("./databases")

with open("./data/fight_config.json", "r") as fight_config_file:
    fight_config: dict = json.load(fight_config_file)

with open("./data/default_messages.json", "r") as default_messages_file:
    default_messages: dict = json.load(default_messages_file)

with open("./data/usage_info", "r") as usage_info_file:
    usage_info: str = usage_info_file.read()

base_dict_loader: dict = {
    "title": discord.Embed.Empty,
    "author_name": "",
    "author_icon_url": discord.Embed.Empty,
    "image": discord.Embed.Empty,
    "thumbnail": discord.Embed.Empty,
    "colour": discord.Embed.Empty,
    "description": list(),
    "fields": dict(),
    "footer": discord.Embed.Empty,
    "footer_url": discord.Embed.Empty,
    "navigation": discord.Embed.Empty,
    "page_count": discord.Embed.Empty,
}
