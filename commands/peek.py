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
from discord.ext import commands
import discord

# Local Application Imports
from data.globals import bot, FAILED_EMOJI
from resources.LaminariaCore.utils.discordpy import DPyUtils
from resources.ensure_collection import ensure_collection
from resources.LaminariaDB.Collection import Collection
from resources.LaminariaDB.Document import Document
from tasks.handle_waifu_listing import handle_waifu_listing
from resources.waifu_dict_loaders.listwaifusimage_dict_loader import make_dict_loader as lwi_dict_loader


@bot.command(description="|WAIFU| Shows information about all the characters matching the name given")
async def peek(ctx: commands.Context, *, waifu_name: str):
    """
    Shows panelled informatiom about a waifu from anyone in the database that matches the name given.

    :param commands.Context ctx: The command context
    :param str waifu_name: The waifu to show the information for
    :return None:
    """

    # Send a loading message to the channel, in order to create the message that will be checked by the task.
    dpy_utils: DPyUtils = DPyUtils()
    listing_message: discord.Message = await dpy_utils.send_loading(ctx.channel)

    waifu_collection: Collection = await ensure_collection(str(ctx.guild.id))
    waifu_query: List[Document] = waifu_collection.find(query={"name": waifu_name.lower()})

    if not waifu_query:
        await listing_message.edit(content="No results!", embed=None)
        return await ctx.message.add_reaction(FAILED_EMOJI)

    waifu_list: List[Document] = sorted(waifu_query, key=lambda x: x.content["name"])
    cache_msg: discord.Message = discord.utils.get(bot.cached_messages, id=listing_message.id)
    bot.loop.create_task(handle_waifu_listing(ctx, waifu_list, cache_msg, 1, lwi_dict_loader))
