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
from data.globals import bot, fight_config, FAILED_EMOJI
from resources.waifu_dict_loaders.element_help_dict_loader import make_dict_loader as eh_dict_loader
from resources.LaminariaCore.utils.discordpy import DPyUtils
from tasks.handle_waifu_listing import handle_waifu_listing



@bot.command(description="Shows the list of elements in the game, their descriptions, weaknesses and strengths.",
             aliases=("ehelp",))
async def elementhelp(ctx, element: str = "Pyro"):
    """
    Using dict loaders, shows the list of available elements and their specifications.

    :param commands.Context ctx:
    :param str element: The element show initially.
    :return None:
    """

    dpy_utils: DPyUtils = DPyUtils()
    listing_message: discord.Message = await dpy_utils.send_loading(ctx.channel)
    cache_msg: discord.Message = discord.utils.get(bot.cached_messages, id=listing_message.id)
    element_list: List[str] = [x for x in fight_config["elements"]]

    if element.title() not in element_list:
        await listing_message.edit(content="No results!", embed=None)
        await ctx.message.add_reaction(FAILED_EMOJI)
        return

    bot.loop.create_task(handle_waifu_listing(ctx, element_list, cache_msg,
                                              element_list.index(element.title()) + 1, eh_dict_loader))
