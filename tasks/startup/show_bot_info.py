# -*- coding: utf-8 -*-
"""
This file is distributed as part of the <project_name> Project.
The source code may be available at
https://github.com/MrKelpy/<project_name>

If a license applies for this project, the former can be found
in every distribution, as a "LICENSE" file at top level.
"""

# Built-in Imports
import socket

# Third Party Imports
from discord.ext import commands

# Local Application Imports


async def show_bot_info(bot: commands.Bot):
    """
    Prints out the bot's info
    :return:
    """

    ip = socket.gethostbyname(socket.gethostname())
    dev = await bot.fetch_user(740969223681212507)
    runtime_info = f"Running on {ip} | {socket.gethostname()}"

    print(f"""
{bot.user.name} BOT
{runtime_info}
{"-" * len(runtime_info)}
Dev INFO:
General: Alexandre Silva, Portugal, Lisbon
Email: alexandresilva.coding@gmail.com
Website: https://cutt.ly/alexandresilva
Discord: {dev}
GitHub: https://github.com/MrKelpy""".strip()
          )


