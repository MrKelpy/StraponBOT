# -*- coding: utf-8 -*-
"""
This file is distributed as part of the StraponBOT Project.
The source code may be available at
https://github.com/MrKelpy/StraponBOT

If a license applies for this project, the former can be found
in every distribution, as a "LICENSE" file at top level.
"""

# Built-in Imports
from typing import Optional, List

# Third Party Imports
from discord.ext import commands
import discord

# Local Application Imports


async def get_trigger_message(ctx: commands.Context, waifu_message: discord.Message) -> Optional[discord.Message]:
    """
    Returns the message prior to the given waifu_message.
    :param commands.Context ctx: The command context
    :param discord.Message waifu_message: The reference message.
    :return discord.Message: The message prior to the waifu_message.
    """

    lookup_index: int = 0
    async for message in ctx.channel.history(limit=100):
        if message.id == waifu_message.id:
            waifu_message_range: List[discord.Message] = await ctx.channel.history(limit=lookup_index+2).flatten()
            waifu_trigger_message: discord.Message = waifu_message_range[-1]
            return waifu_trigger_message

        lookup_index += 1
    else:
        return None
