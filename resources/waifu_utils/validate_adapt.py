# -*- coding: utf-8 -*-
"""
This file is distributed as part of the StraponBOT Project.
The source code may be available at
https://github.com/MrKelpy/StraponBOT

If a license applies for this project, the former can be found
in every distribution, as a "LICENSE" file at top level.
"""

# Built-in Imports
from typing import List, Optional, Union

# Third Party Imports
import discord
from discord.ext import commands

# Local Application Imports
from resources.LaminariaDB.LaminariaDB import Collection
from resources.LaminariaDB.Document import Document
from resources.ensure_collection import ensure_collection
from resources.waifu_utils.validate_basics import validate_basics


async def check_for_reclaim(trigger_message: discord.Message, waifu_document: Document) -> bool:
    """
    Checks if the user is trying to reclaim a waifu that is now theirs.
    :param trigger_message: The message prior to the waifu_message.
    :param Document waifu_document: The document from the database referring to the waifu
    :return bool: True if the user is trying to reclaim a waifu, false otherwise.
    """

    if trigger_message.author.id != waifu_document.content["owner"]:
        return True

    return False


async def validate_waifu(ctx: commands.Context) -> Union[Optional[discord.Message], Document]:
    """
    Checks if the last message came from Mudae, and contains valid waifu that isn't already in the database.
    :return Union[Optional[discord.Message], int]: The waifu message if valid, or the Document.
    """

    # Check if the message is replying to something. If so, make it the last message.
    if ctx.message.reference:
        waifu_message: discord.Message = await ctx.channel.fetch_message(ctx.message.reference.message_id)

    else:
        waifu_message: List[discord.Message] = await ctx.channel.history(limit=2).flatten()
        waifu_message: discord.Message = waifu_message[-1]

    # Performs a basic waifu message validation.
    waifu_trigger_message: discord.Message = await validate_basics(ctx, waifu_message)
    if not waifu_trigger_message: return

    # Makes sure that the waifu is not already in the database. (True if not)
    waifus_collection: Collection = await ensure_collection(str(ctx.guild.id))
    waifu_document: List[Document] = waifus_collection.find(query={"name": waifu_message.embeds[0].author.name.lower()},
                                                            limit=1)

    # Checks if the user is trying to reclaim a waifu, in which case, returns the document.
    if waifu_document and await check_for_reclaim(waifu_trigger_message, waifu_document[0]):
        return waifu_document[0]

    # If the waifu is not in the database, and the user is not trying to reclaim, then it is a new waifu.
    return waifu_message if not waifu_document else None
