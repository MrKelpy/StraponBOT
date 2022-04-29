# -*- coding: utf-8 -*-
"""
This file is distributed as part of the StraponBOT Project.
The source code may be available at
https://github.com/MrKelpy/StraponBOT

If a license applies for this project, the former can be found
in every distribution, as a "LICENSE" file at top level.
"""

# Built-in Imports
# Third Party Imports
import discord

# Local Application Imports
from data.embeds import waifu_listing_embed_build


async def parse_dict_loader(dict_loader: dict) -> discord.Embed:
    """
    Iterates over the dict_loader parameters amd creates an embed with the information
    of a waifu.
    :param dict dict_loader: The dictionary containing information for the embed to be loaded with.
    This "dict_loader" follows a common pattern that is recognised by this function. It tells the function
    what should go into the embed title, with the "title" key, what should go into the description, using the "description"
    key, and what should go into the fields of the embed, with the "fields" key.

    :return None:
    """

    # Loads the title into the embed
    waifu_listing_embed: discord.Embed = waifu_listing_embed_build.copy()
    waifu_listing_embed.title = dict_loader["title"]
    waifu_listing_embed.description = ""

    # Loads the description values into the embed
    for value in dict_loader["description"]:
        waifu_listing_embed.description += f"{value.strip()}\n"
    waifu_listing_embed.description = waifu_listing_embed.description.strip()  # Removes any trailing whitespaces or breaks

    # Loads the fields into the embed
    for value in dict_loader["fields"]:
        waifu_listing_embed.add_field(name=value, value=dict_loader["fields"][value], inline=True)

    # Loads the image and thumbnail into the embed
    waifu_listing_embed.set_image(url=dict_loader["image"])
    waifu_listing_embed.set_thumbnail(url=dict_loader["thumbnail"])

    # Sets the embed colour, the footer and author into the embed
    waifu_listing_embed.set_footer(text=dict_loader["footer"], icon_url=dict_loader["footer_url"])
    waifu_listing_embed.set_author(name=dict_loader["author_name"], icon_url=dict_loader["author_icon_url"])
    waifu_listing_embed.colour = dict_loader["colour"]

    return waifu_listing_embed
