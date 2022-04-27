# -*- coding: utf-8 -*-
"""
This file is distributed as part of the StraponBOT Project.
The source code may be available at
https://github.com/MrKelpy/StraponBOT

If a license applies for this project, the former can be found
in every distribution, as a "LICENSE" file at top level.
"""

# Built-in Imports
from typing import List, Union, Tuple

# Third Party Imports
import discord
from discord.ext import commands

# Local Application Imports
from resources.LaminariaCore.utils.discordpy import DPyUtils
from resources.LaminariaDB.Collection import Collection
from resources.LaminariaDB.Document import Document
from resources.ensure_collection import ensure_collection
from data.globals import FAILED_EMOJI


async def do_prelisting_jobs(ctx: commands.Context, starting_index: int) -> Union[bool, Tuple[List[Document], discord.Message]]:
    """
    Performs pre-listing jobs such as checking the inputs to the command
    and other tasks that need to be done before every listing command shows their list.

    :param commands.Context ctx: The context of the command.
    :param int starting_index: The index of the first item to be listed.
    :return bool: Whether the checks passed or not
    """

    # Send a loading message to the channel, in order to create the message that will be checked by the task.
    dpy_utils: DPyUtils = DPyUtils()
    listing_message: discord.Message = await dpy_utils.send_loading(ctx.channel)

    waifu_collection: Collection = await ensure_collection(str(ctx.guild.id))
    waifu_query: List[Document] = waifu_collection.find(query={"owner": ctx.author.id})

    # Prevents an user from typing in a starting index that is too high or too low.
    if starting_index < 1 or starting_index > len(waifu_query):
        await listing_message.delete()
        await ctx.message.add_reaction(FAILED_EMOJI)
        return False

    # Lets the user know that they don't have any adapted waifus.
    if not waifu_query:
        await listing_message.delete()
        await ctx.send(f"No results.")
        return False

    return waifu_query, listing_message
