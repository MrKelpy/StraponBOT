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
# Local Application Imports
from resources.waifu_utils.fix_navigation_header import fix_navigation_header
from resources.waifu_utils.get_element_weaknesses import get_element_weaknesses
from data.globals import base_dict_loader, fight_config, bot


async def make_dict_loader(elements_list: List[str], navigation_header: int, next_page: bool) -> dict:
    """
    Makes a specific dict loader for the "elements" command. This dict loader
    is designed to contain the specifications for each element in the fight_config file.

    :param List[str] elements_list: A list of the existent elements in the game.
    :param int navigation_header: The navigation header for the paging
    :param bool next_page: Whether the dict loader should load the next item in the list or the previous.
    :return dict: The dict loader response
    """

    # Preparing the basic stuff
    navigation_header: int = await fix_navigation_header(next_page, navigation_header, len(elements_list))
    dict_loader: dict = base_dict_loader.copy()
    dict_loader["navigation"] = navigation_header

    # Loading the basics of the embed
    element_icon: str = fight_config["elements"][elements_list[navigation_header-1]]["emoji"]
    element_dict: dict = fight_config["elements"][elements_list[navigation_header-1]]
    dict_loader["title"] = f"{element_icon} {elements_list[navigation_header-1]} - Specifications"
    dict_loader["thumbnail"] = bot.get_emoji(int(element_icon.split(":", 2)[-1][:-1])).url
    dict_loader["colour"] = int("ffffff", 16)
    dict_loader["footer"] = f"Page {navigation_header}/{len(elements_list)}"

    # Building and loading the description
    strengths: List[str] = element_dict["strong_against"]
    weaknesses: List[str] = await get_element_weaknesses(elements_list[navigation_header-1])
    dict_loader["description"] = [element_dict["description"]]
    dict_loader["fields"] = {"Strong Against": "\n".join(strengths) if strengths else "Nothing",
                             "Weak Against": "\n".join(weaknesses) if weaknesses else "Nothing"}

    return dict_loader
