# -*- coding: utf-8 -*-
"""
This file is distributed as part of the StraponBOT Project.
The source code may be available at
https://github.com/MrKelpy/StraponBOT

If a license applies for this project, the former can be found
in every distribution, as a "LICENSE" file at top level.
"""

# Built-in Imports
from typing import List, Optional

# Third Party Imports
import discord
from discord.ext import commands

# Local Application Imports
from data.globals import MUDAE_ID
from resources.LaminariaDB.LaminariaDB import Collection
from resources.ensure_collection import ensure_collection


async def get_trigger_message(ctx: commands.Context, waifu_message: discord.Message) -> Optional[discord.Message]:
    """
    Returns the message prior to the given waifu_message.
    :param commands.Context ctx: The command context
    :param discord.Message waifu_message: The reference message.
    :return discord.Message: The message prior to the waifu_message.
    """

    lookup_index: int = 0
    async for message in ctx.channel.history(limit=None):
        if message.id == waifu_message.id:
            waifu_message_range: List[discord.Message] = await ctx.channel.history(limit=lookup_index+2).flatten()
            waifu_trigger_message: discord.Message = waifu_message_range[-1]
            return waifu_trigger_message

        lookup_index += 1
    else:
        return None


async def validate_waifu(ctx: commands.Context) -> Optional[discord.Message]:
    """
    Checks if the last message came from Mudae, and contains valid waifu that isn't already in the database.
    :return bool: True if the last message came from Mudae, and contains a valid waifu.
    """

    # Check if the message is replying to something. If so, make it the last message.
    if ctx.message.reference:
        waifu_message: discord.Message = await ctx.channel.fetch_message(ctx.message.reference.message_id)

    else:
        waifu_message: List[discord.Message] = await ctx.channel.history(limit=2).flatten()
        waifu_message: discord.Message = waifu_message[-1]

    if not waifu_message.author.id == MUDAE_ID:
        return None

    # Get the message prior to the last message.
    waifu_trigger_message: discord.Message = await get_trigger_message(ctx, waifu_message)

    # Make sure that the user isn't trying to use the mmi on someone else's harem.
    trigger_message_validation: bool = not waifu_trigger_message.mentions and \
                                       waifu_trigger_message.content.startswith("$mmi")

    # Make sure that the last message is a waifu message.
    waifu_message_validation: bool = waifu_message.embeds and waifu_message.author.id == MUDAE_ID

    # Makes sure that the waifu is not already in the database. (True if not)
    waifus_collection: Collection = await ensure_collection(str(ctx.guild.id))
    duplicate_validation: bool = not waifus_collection.find(query={"name": waifu_message.embeds[0].author.name.lower()},
                                                            limit=1)
    # If either validation fails, return False.
    if not trigger_message_validation or not waifu_message_validation or not duplicate_validation:
        return None

    return waifu_message
