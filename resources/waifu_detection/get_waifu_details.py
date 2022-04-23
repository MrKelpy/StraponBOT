# -*- coding: utf-8 -*-
"""
This file is distributed as part of the StraponBOT Project.
The source code may be available at
https://github.com/MrKelpy/StraponBOT

If a license applies for this project, the former can be found
in every distribution, as a "LICENSE" file at top level.
"""

# Built-in Imports
from typing import List, Dict
import re

# Third Party Imports
import discord
from discord.ext import commands

# Local Application Imports

async def get_source(description: str) -> str:
    """
    Parses out the anime/game source line from the waifu embed.
    :param str description: The embed description
    :return str: The anime/game source line
    """

    source: str = ""
    for line in description.split("\n"):

        # If the line contains the "Animanga Roulette" excerpt which comes after the source, we're done.
        if "Animanga roulette" in line:
            break
        source += f"{line} "

    return source.strip()


async def get_waifu_details(ctx: commands.Context) -> Dict[str, object]:
    """
    Once a waifu has been validated, this function will return its details, in the form of a dict.
    :param commands.Context ctx: The command context
    :return Dict: The waifu details dict
    """

    # Like in the validate_waifu function, we need to get the waifu message. However, this time,
    # we are guaranteed the position of the waifu message, since it's already been validated.
    waifu_message: List[discord.Message] = await ctx.channel.history(limit=2).flatten()
    waifu_message: discord.Message = waifu_message[-1]
    kakera_value_line: str = [x for x in waifu_message.embeds[0].description.split("\n") if "Animanga roulette" in x][0]
    source: str = await get_source(waifu_message.embeds[0].description)

    waifu_details: dict = {
        "name": waifu_message.embeds[0].author.name,
        "source": source.split("<")[0].strip(),
        "image": waifu_message.embeds[0].image.url,
        "embed_colour": waifu_message.embeds[0].colour.value,
        "kakera_value": int(re.search(r"\d+", kakera_value_line).group(0)),
        "gender": "female" if "female" in source else "male"
    }

    return waifu_details
