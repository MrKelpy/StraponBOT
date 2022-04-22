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
from data.globals import bot
from resources.ensure_collection import ensure_collection
from resources.LaminariaDB.Collection import Collection
from resources.LaminariaDB.Document import Document
from resources.LaminariaCore.utils.discordpy import DPyUtils
from tasks.waifu_listing.handle_imaged_listing import handle_waifu_listing


@bot.command(description="Lists all the adapted waifus and their perks to an user.", aliases=("lwi",))
async def listwaifusimage(ctx: commands.Context, starting_index: int = 1, member: discord.Member = None, ) -> None:
    """
    Accesses the database and runs through all the waifus, and returns a list of the waifus owned
    by the user. Then, sorts them alphabetically, and sends the list into a task that will handle
    showing the list to the user through embeds.
    If the list comes out empty, let the user know they have no waifus.

    :param command.Context ctx: The command context
    :param discord.Member member: The user to list waifus for. Defaults to the author of the command.
    :param int starting_index: The index of the waifu to start at.
    :return None:
    """

    if member is None:
        member: discord.Member = ctx.author

    # Send a loading message to the channel, in order to create the message that will be checked by the task.
    dpy_utils: DPyUtils = DPyUtils()
    listing_message: discord.Message = await dpy_utils.send_loading(ctx.channel)

    waifu_collection: Collection = await ensure_collection(str(ctx.guild.id))
    waifu_query: List[Document] = waifu_collection.find(query={"owner": member.id})

    if not waifu_query:
        await listing_message.delete()
        await ctx.send(f"No results.")
        return

    waifu_list: List[Document] = sorted(waifu_query, key=lambda x: x.content["name"])
    cache_msg: discord.Message = discord.utils.get(bot.cached_messages, id=listing_message.id)
    bot.loop.create_task(handle_waifu_listing(ctx, waifu_list, cache_msg, starting_index-1))
