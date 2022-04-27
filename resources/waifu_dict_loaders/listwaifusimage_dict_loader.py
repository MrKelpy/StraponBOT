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

# Local Application Imports
from resources.LaminariaDB.Document import Document
from data.globals import fight_config, bot


async def make_dict_loader(waifu_document_list: List[Document], navigation_header: int) -> dict:
    """
    Creates a specific dict loader for the "listwaifusimage" command.
    This dict loader will create panels for the given waifu at the time, with all of their stats and
    picture, everything.

    :param Document waifu_document_list: The list of waifus to deal with
    :param int navigation_header: The navigation header pointing to our current position in the visual list
    :return dict: The dict loader for the "listwaifusimage" command
    """

    # Store the element icon in a variable for readability
    waifu_document: Document = waifu_document_list[0]
    element_icon: str = fight_config['elements'][waifu_document.content['element']]['emoji']

    # Create a dict to store the data we want to return and set the basic values (title and colour)
    dict_loader: dict = dict()
    dict_loader["title"] = waifu_document.content["name"]
    dict_loader["colour"] = waifu_document.content["embed_colour"]

    # Adds the description values into the dict loader
    dict_loader["description"] = list()
    dict_loader["description"].append(f"{waifu_document.content['source']} :{waifu_document.content['gender']}_sign:\n")
    dict_loader["description"].append(f"LEVEL: {waifu_document.content['level']} "
                                      f"({waifu_document.content['exp']}/{waifu_document.content['next_level']})\n")
    dict_loader["description"].append(f"CLASS: {waifu_document.content['class']} | "
                                      f"{waifu_document.content['element']} {element_icon}\n")
    dict_loader["description"].append(f"SKILL POINTS: {waifu_document.content['skill_points']}\n")
    dict_loader["description"].append(f"HP: {waifu_document.content['max_hp']}")

    # Adds the field values into the dict loader
    dict_loader["fields"] = dict()
    dict_loader["fields"]["Physical Damage"] = waifu_document.content["physical_dmg"]
    dict_loader["fields"]["Magical Damage"] = waifu_document.content["magical_dmg"]
    dict_loader["fields"]["Physical Defense"] = waifu_document.content["physical_def"]
    dict_loader["fields"]["Magical Defense"] = waifu_document.content["magical_def"]
    dict_loader["fields"]["Speed"] = waifu_document.content["speed"]
    dict_loader["fields"]["Luck"] = waifu_document.content["luck"]

    # Adds the extra information values into the dict loader
    author: discord.Member = bot.get_user(waifu_document.content["owner"])
    dict_loader["image"] = waifu_document.content["image"]
    dict_loader["page_count"] = len(waifu_document_list)
    dict_loader["navigation"] = navigation_header
    dict_loader["footer"] = f"Belongs to {author.name} -- {navigation_header}/{len(waifu_document_list)}"

    return dict_loader
