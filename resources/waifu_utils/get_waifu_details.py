# -*- coding: utf-8 -*-
"""
This file is distributed as part of the StraponBOT Project.
The source code may be available at
https://github.com/MrKelpy/StraponBOT

If a license applies for this project, the former can be found
in every distribution, as a "LICENSE" file at top level.
"""

# Built-in Imports
from typing import Dict
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


async def get_waifu_details(ctx: commands.Context, waifu_message: discord.Message) -> Dict[str, object]:
    """
    Once a waifu has been validated, this function will return its details, in the form of a dict.
    :param commands.Context ctx: The command context
    :param discord.Message waifu_message: The message containing the waifu embed
    :return Dict: The waifu details dict
    """

    kakera_value_line: str = [x for x in waifu_message.embeds[0].description.split("\n") if "Animanga roulette" in x or "Game roulette" in x][0]
    source: str = await get_source(waifu_message.embeds[0].description)

    waifu_details: dict = {
        "name": waifu_message.embeds[0].author.name.lower(),
        "source": source.split("<")[0].strip(),
        "image": waifu_message.embeds[0].image.url,
        "embed_colour": waifu_message.embeds[0].colour.value,
        "kakera_value": int(re.search(r"\d+", kakera_value_line).group(0)),
        "gender": "female" if "female" in source else "male"
    }

    return waifu_details
