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
from resources.waifu_utils.do_prelisting_jobs import do_prelisting_jobs
from resources.LaminariaDB.Document import Document
from tasks.handle_waifu_listing import handle_waifu_listing
from resources.waifu_dict_loaders.listwaifus_dict_loader import make_dict_loader as lw_dict_loader


@bot.command(description="|LISTING| Lists all of the waifus in the database for a given user based on their luck",
             aliases=("lwluck",))
async def listwaifusluck(ctx: commands.Context, starting_index: int = 1):
    """
    Lists all the waifus in the database for a given user, in a paged list of 15 waifus per, based
    on their luck.

    :param commands.Context ctx: The command context
    :param int starting_index: The starting index for the paged list.
    :return None:
    """

    waifu_query, listing_message = await do_prelisting_jobs(ctx, starting_index)
    if not waifu_query: return
    if starting_index < 0: starting_index = 1

    waifu_list: List[Document] = sorted(waifu_query, key=lambda x: x.content["luck"], reverse=True)
    cache_msg: discord.Message = discord.utils.get(bot.cached_messages, id=listing_message.id)
    bot.loop.create_task(handle_waifu_listing(ctx, waifu_list, cache_msg, starting_index, lw_dict_loader))
