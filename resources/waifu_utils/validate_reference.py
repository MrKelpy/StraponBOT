# -*- coding: utf-8 -*-
"""
This file is distributed as part of the StraponBOT Project.
The source code may be available at
https://github.com/MrKelpy/StraponBOT

If a license applies for this project, the former can be found
in every distribution, as a "LICENSE" file at top level.
"""

# Built-in Imports
# Third Party Imports
from discord.ext import commands
import discord

# Local Application Imports
from resources.waifu_utils.get_trigger_message import get_trigger_message


async def validate_reference(ctx: commands.Context) -> bool:
    """
    Validates whether the reference message is a valid waifu

    :param commands.Context ctx: The command context
    :return None:
    """

    waifu_message: discord.Message = ctx.message.reference
    if not waifu_message: return False

    waifu_embed_validation: bool = waifu_message.author.id == 432610292342587392
    trigger_message: discord.Message = await get_trigger_message(ctx, waifu_message)
    if not trigger_message: return False

    waifu_trigger_validation: bool = trigger_message.mentions == 0 and trigger_message.author.id == ctx.author.id and \
                                     trigger_message.content.startswith("$lwi") or trigger_message.content.startswith("$mmi")

    if not (waifu_embed_validation and waifu_trigger_validation):
        return False

    return True



