# -*- coding: utf-8 -*-
"""
This file is distributed as part of the StraponBOT Project.
The source code may be available at
https://github.com/MrKelpy/StraponBOT

If a license applies for this project, the former can be found
in every distribution, as a "LICENSE" file at top level.
"""

# Built-in Imports
from typing import Optional

# Third Party Imports
from discord.ext import commands
import discord

# Local Application Imports
from resources.waifu_utils.get_trigger_message import get_trigger_message
from data.globals import MUDAE_ID, bot


async def validate_basics(ctx: commands.Context, waifu_message: discord.Message) -> Optional[discord.Message]:
    """
    Validates the basics of every type of waifu validation existent in the bot.
    Essentially, validates if the both the trigger message and the waifu are valid.

    :param commands.Context ctx: The command context
    :param discord.Message waifu_message: The message containing the waifu embed
    :return discord.Message: The waifu trigger message.
    """

    waifu_trigger_message: discord.Message = await get_trigger_message(ctx, waifu_message)
    if not waifu_trigger_message: return None

    # Make sure that the user isn't trying to use the mmi on someone else's harem.
    trigger_message_validation: bool = not waifu_trigger_message.mentions and waifu_trigger_message.author.id == ctx.author.id and \
                                       waifu_trigger_message.content.startswith("$mmi") or\
                                       waifu_trigger_message.content.startswith("$lwi") or \
                                       waifu_trigger_message.content.startswith("$peek")

    waifu_message_validation: bool = waifu_message.author.id == MUDAE_ID or waifu_message.author.id == bot.user.id \
                                     and waifu_message.embeds

    if not (trigger_message_validation and waifu_message_validation):
        return None

    return waifu_trigger_message
