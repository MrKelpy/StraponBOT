# -*- coding: utf-8 -*-
"""
This file is distributed as part of the StraponBOT Project.
The source code may be available at
https://github.com/MrKelpy/StraponBOT

If a license applies for this project, the former can be found
in every distribution, as a "LICENSE" file at top level.
"""

# Built-in Imports
from typing import List

# Third Party Imports
import discord
from discord.ext import commands

# Local Application Imports
from data.globals import MUDAE_ID


async def validate_waifu(ctx: commands.Context) -> bool:
    """
    Checks if the last message came from Mudae, and contains valid waifu.
    :return bool: True if the last message came from Mudae, and contains a valid waifu.
    """

    # Get both the last message, which will be a waifu message and the trigger command
    # for that message.
    last_message: List[discord.Message] = await ctx.channel.history(limit=2).flatten()
    last_message: discord.Message = last_message[-1]

    waifu_trigger_message: List[discord.Message] = await ctx.channel.history(limit=3).flatten()
    waifu_trigger_message: discord.Message = waifu_trigger_message[-1]

    if not last_message.author.id == MUDAE_ID:
        return False

    # Make sure that the user isn't trying to use the mmi on someone else's harem.
    trigger_message_validation: bool = not waifu_trigger_message.mentions and \
                                       waifu_trigger_message.content.startswith("$mmi")

    # Make sure that the last message is a waifu message.
    last_message_validation: bool = last_message.embeds and last_message.author.id == MUDAE_ID

    # If either validation fails, return False.
    if not trigger_message_validation or not last_message_validation:
        return False

    return True
