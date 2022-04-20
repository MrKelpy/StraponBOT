# -*- coding: utf-8 -*-
"""
This file is distributed as part of the <project_name> Project.
The source code may be available at
https://github.com/MrKelpy/<project_name>

If a license applies for this project, the former can be found
in every distribution, as a "LICENSE" file at top level.
"""

# Built-in Imports
import os
import signal

# Third Party Imports
# Local Application Imports
import discord

from tasks.startup.show_bot_info import show_bot_info
from tasks.startup.register_commands import register_commands
from tasks.startup.register_events import register_events
from data.globals import bot, token, prefix


@bot.event
async def on_ready():
    """
    Detects when the bot goes online and runs any
    startup functions needed for the bot's functionment.
    The two compulsory functions to be run are the functions that register the commands
    and show the bot's info.
    :return:
    """

    # Set the activity to have the prefix
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,
                                                        name=f"{prefix}"))

    # Compulsory functions
    await register_events()
    await register_commands()
    await show_bot_info(bot)


if __name__ == "__main__":
    try:
        bot.remove_command("help")
        bot.run(token)
    except KeyboardInterrupt:
        os.kill(os.getpid(), signal.SIGTERM)
