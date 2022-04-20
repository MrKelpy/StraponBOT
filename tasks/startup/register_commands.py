# -*- coding: utf-8 -*-
"""
This file is distributed as part of the <project_name> Project.
The source code may be available at
https://github.com/MrKelpy/<project_name>

If a license applies for this project, the former can be found
in every distribution, as a "LICENSE" file at top level.
"""

# Built-in Imports
import importlib

# Third Party Imports
# Local Application Imports
import os


async def register_commands():
    """
    Due to the design of the bot, this function is needed to register any commands
    that are declared outside of bot.py.
    This function simply imports all the files where the commands are located, so that
    they get registered within discord.py.
    :return:
    """

    commands_location = "./commands"  # Relative path from bot.py (Entrypoint) to bot/commands.
    commands = [f"commands.{cmd.split('.')[0]}" for cmd in os.listdir(commands_location) if cmd.endswith(".py")]

    for command in commands:
        importlib.import_module(command)