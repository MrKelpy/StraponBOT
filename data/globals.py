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

# Third Party Imports
from discord.ext import commands as cmds
from discord import Intents

# Local Application Imports
from resources.config_handler.load_settings import load_settings
from resources.LaminariaCore.utils.discordpy import DPyUtils
from resources.LaminariaDB.LaminariaDB import LaminariaDB

settings: Dict[str, str] = load_settings("./data/bot.config")
token: str = settings["token"]
prefix: str = settings["prefix"]
intents = Intents.default()
bot: cmds.Bot = cmds.Bot(command_prefix=prefix, intents=intents)
dpyutils: DPyUtils = DPyUtils()
MUDAE_ID: int = 432610292342587392
FAILED_EMOJI: str = "❌"
SUCCESS_EMOJI: str = "✅"
waifus_db: LaminariaDB = LaminariaDB("./databases")
