# -*- coding: utf-8 -*-
"""
This file is distributed as part of the StraponBOT Project.
The source code may be available at
https://github.com/MrKelpy/StraponBOT

If a license applies for this project, the former can be found
in every distribution, as a "LICENSE" file at top level.
"""

# Built-in Imports
from typing import List, Tuple, Callable
from datetime import datetime

# Third Party Imports
from discord.ext import commands
import discord
import asyncio

# Local Application Imports
from resources.LaminariaDB.Document import Document
from resources.waifu_utils.parse_dict_loader import parse_dict_loader
from data.globals import NEXT_EMOJI, PREV_EMOJI


async def process_reactions(ctx: commands.Context, reaction: discord.Reaction, waifu_list: List[Document],
                            navigation_header: int, listing_message: discord.Message, dict_loader_func: Callable,
                            next_page: bool) -> Tuple[float, int]:
    """
    Processes the reaction of the user, moving on to the next waifu or returning to the previous waifu.

    :param commands.Context ctx: The command context
    :param discord.Reaction reaction: The reaction that was added
    :param List[Document] waifu_list: The list of waifus that the user has
    :param int navigation_header: The navigation header pointing to the current position in the
    visual list that the user is in
    :param discord.Message listing_message: The waifu listing message to edit and work with
    :param dict dict_loader_func: The dict loader to use to format the waifu embed
    :param bool next_page: Whether or not the user is requesting the next or prior page

    :return float, int: The new timeout timestamp (+30s), the new navigation header
    """

    async for user in reaction.users():  # Removes the reaction from every user but the bot
        if user.id == 966370729597730966: continue
        await listing_message.remove_reaction(reaction.emoji, user)

    dict_loader: dict = await dict_loader_func(waifu_list, navigation_header, next_page)  # Creates the dict loader
    await listing_message.edit(embed=await parse_dict_loader(dict_loader))  # Edits the message
    return datetime.now().timestamp() + 30.0, dict_loader['navigation']  # Returns the new timestamp and header


async def handle_waifu_listing(ctx: commands.Context, waifu_list: list,
                               listing_message: discord.Message, starting_index: int, dict_loader_func: Callable):
    """
    Handles the listing of an user's waifus. This function will listen for any reactions added to the message
    every .05 seconds, and show the next/prior waifu in the list accordingly to the reaction. The waifus will be
    shown alongside all their stats. The listing will stop working after a timeout of 30s.

    :param discord.Message listing_message: The message to be edited with the waifus
    :param commands.Context ctx: The command context
    :param List[Document] waifu_list: A list of documents from the database containing all of the waifus for the user.
    :param int starting_index: The index of the waifu to start the listing with.
    :param Callable dict_loader_func: The dict loader function to be used to format the waifu embed.

    :return None:
    """

    timeout_stamp: float = datetime.now().timestamp() + 30.0
    navigation_header: int = starting_index

    dict_loader_data: dict = await dict_loader_func(waifu_list, navigation_header-1, True)  # Creates the dict loader
    first_listing: discord.Embed = await parse_dict_loader(dict_loader_data)

    await listing_message.edit(embed=first_listing)  # Edits the embed with a waifu from the starting index to display
    await listing_message.add_reaction(PREV_EMOJI)
    await listing_message.add_reaction(NEXT_EMOJI)

    # Listens for any reactions added to the message every .05 seconds
    while datetime.now().timestamp() <= timeout_stamp:
        for reaction in listing_message.reactions:

            if reaction.emoji == NEXT_EMOJI and reaction.count > 1:  # Checks if the reaction is the "next" emoji
                timeout_stamp, navigation_header = await process_reactions(ctx, reaction, waifu_list, navigation_header,
                                                                           listing_message, dict_loader_func, True)

            elif reaction.emoji == PREV_EMOJI and reaction.count > 1:  # Checks if the reaction is the "previous" emoji
                timeout_stamp, navigation_header = await process_reactions(ctx, reaction, waifu_list, navigation_header,
                                                                           listing_message, dict_loader_func, False)

            await asyncio.sleep(0.01)

    # Edits the embed to show that the listing is locked when the timeout is reached
    listing_message.embeds[0].set_footer(text=listing_message.embeds[0].footer.text + " 🔒 Locked",
                                         icon_url=listing_message.embeds[0].footer.icon_url)
    await listing_message.edit(embed=listing_message.embeds[0])
