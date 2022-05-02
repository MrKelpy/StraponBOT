# -*- coding: utf-8 -*-
"""
This file is distributed as part of the StraponBOT Project.
The source code may be available for the public at
https://github.com/MrKelpy/StraponBOT

If a license applies for this project, the former can be found
in every distribution, as a "LICENSE" file at top level.
"""

# Built-in Imports
# Third Party Imports
# Local Application Imports
from data.globals import bot


@bot.event
async def on_message(message):
    """
    Handles any functions that should happen whenever a message is sent
    to the chat.
    :param discord.Message message: The sent message
    :return None:
    """

    if message.author.bot or "hell" in message.channel.name:
        return

    if "dead" in [role.name for role in message.author.roles]:
        await message.delete()

    await bot.process_commands(message)

