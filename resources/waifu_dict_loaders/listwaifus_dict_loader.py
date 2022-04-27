# -*- coding: utf-8 -*-
"""
This file is distributed as part of the StraponBOT Project.
The source code may be available at
https://github.com/MrKelpy/StraponBOT

If a license applies for this project, the former can be found
in every distribution, as a "LICENSE" file at top level.
"""

# Built-in Imports
from more_itertools import chunked
from typing import List

# Third Party Imports
import discord

# Local Application Imports
from resources.LaminariaDB.Document import Document
from resources.waifu_utils.fix_navigation_header import fix_navigation_header
from data.globals import bot, base_dict_loader


async def make_dict_loader(waifu_document_list: List[Document], navigation_header: int, next_page: bool) -> dict:
    """
    Makes a specific dict loader for the "listwaifus" command.
    This dict loader will show a list of the waifus in the database for the given user.

    :param List[Document] waifu_document_list: The Document in the database representing the waifu.
    :param int navigation_header: The navigation header pointing to our current position in the visual list
    :param bool next_page: Whether the listing should go to the next or prior page
    :return None:
    """

    # Create a dict to store the data we want to return.
    dict_loader: dict = base_dict_loader.copy()

    # Set the basic values
    author: discord.Member = bot.get_user(waifu_document_list[0].content["owner"])
    dict_loader["title"] = f"{author.name}'s Harem"
    dict_loader["author"] = author
    dict_loader["colour"] = discord.Colour.dark_red()

    # Prepare the description and page count to set it into the embed
    chunked_waifu_list: List[List[str]] = list(chunked([x.content["name"] for x in waifu_document_list], 15))
    page_count: int = len(chunked_waifu_list) + 1 if not float(len(chunked_waifu_list)).is_integer() \
        else len(chunked_waifu_list)

    navigation_header = await fix_navigation_header(next_page, navigation_header, page_count)
    dict_loader["navigation"] = navigation_header

    # Set the description, footer and thumnbnail into the dict loader
    dict_loader["description"] = chunked_waifu_list[navigation_header-1]
    dict_loader["footer"] = f"Page {navigation_header}/{page_count}"

    # Get the image from the waifu_document_list of the waifu with the same name as the first in the chunked list
    # and set it as the thumbnail
    dict_loader["thumbnail"] = [x.content["image"] for x in waifu_document_list
                                if x.content["name"] == chunked_waifu_list[navigation_header-1][0]][0]

    return dict_loader
