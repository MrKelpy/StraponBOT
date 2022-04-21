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
import re

# Third Party Imports
import discord
from discord.ext import commands

# Local Application Imports


async def get_waifu_details(ctx: commands.Context) -> dict:
    """
    Once a waifu has been validated, this function will return its details, in the form of a dict.
    :param ctx:
    :return:
    """

    # Like in the validate_waifu function, we need to get the waifu message. However, this time,
    # we are guaranteed the position of the waifu message, since it's already been validated.
    waifu_message: List[discord.Message] = await ctx.channel.history(limit=2).flatten()
    waifu_message: discord.Message = waifu_message[-1]

    waifu_details: dict = {
        "name": waifu_message.embeds[0].author.name,
        "source": waifu_message.embeds[0].description.split("\n")[0],
        "image": waifu_message.embeds[0].image.url,
        "kakera_value": re.match(r"/^[1-9]\d*$/", waifu_message.embeds[0].description.split("\n")[1]),
    }

    return waifu_details
