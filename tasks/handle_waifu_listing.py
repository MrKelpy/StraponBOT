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
from resources.waifu_utils.load_waifu_listing import load_waifu_listing
from data.globals import NEXT_EMOJI, PREV_EMOJI


async def update_header(waifu_list: List[Document], increment: bool, current: int) -> int:
    """
    Checks whether the header should be incremented or decremented and returns the new header.
    If one of the ends of the list is reached, loop around.
    :param List[Document] waifu_list: The waifu list of the user
    :param bool increment: Whether to increment or decrement the header
    :param int current: The current value of the header
    :return int: The new value of the header
    """

    if increment and current == len(waifu_list):  # The update is incrementing and we're at the end of the list
        return 1

    if not increment and current == 1:  # The update is decrementing and we're at the first waifu
        return len(waifu_list)

    return current + 1 if increment else current - 1


async def process_reactions(ctx: commands.Context, reaction: discord.Reaction, waifu_list: List[Document],
                            navigation_header: int, listing_message: discord.Message, increment: bool,
                            dict_loader_func: Callable) -> Tuple[float, int]:
    """
    Processes the reaction of the user, moving on to the next waifu or returning to the previous waifu.

    :param commands.Context ctx: The command context
    :param discord.Reaction reaction: The reaction that was added
    :param List[Document] waifu_list: The list of waifus that the user has
    :param int navigation_header: The navigation header pointing to the current position in the
    visual list that the user is in
    :param discord.Message listing_message: The waifu listing message to edit and work with
    :param bool increment: Whether to increment or decrement the header
    :param dict dict_loader_func: The dict loader to use to format the waifu embed

    :return float, int: The new timeout timestamp (+30s), the new navigation header
    """

    navigation_header = await update_header(waifu_list, increment, navigation_header)  # Updates the navigation header

    async for user in reaction.users():  # Removes the reaction from every user but the bot
        if user.id == 966370729597730966: continue
        await listing_message.remove_reaction(reaction.emoji, user)

    dict_loader: dict = await dict_loader_func(waifu_list[0], navigation_header, len(waifu_list))  # Creates the dict loader
    await listing_message.edit(embed=await load_waifu_listing(ctx, dict_loader))  # Edits the message
    return datetime.now().timestamp() + 30.0, navigation_header


async def handle_waifu_listing(ctx: commands.Context, waifu_list: List[Document],
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
    navigation_header: int = starting_index + 1

    dict_loader_data: dict = await dict_loader_func(waifu_list, navigation_header)  # Creates the dict loader
    first_waifu: discord.Embed = await load_waifu_listing(ctx, dict_loader_data)

    await listing_message.edit(embed=first_waifu)  # Edits the embed with a waifu from the starting index to display
    await listing_message.add_reaction(PREV_EMOJI)
    await listing_message.add_reaction(NEXT_EMOJI)

    # Listens for any reactions added to the message every .05 seconds
    while datetime.now().timestamp() <= timeout_stamp:
        for reaction in listing_message.reactions:

            if reaction.emoji == NEXT_EMOJI and reaction.count > 1:  # Checks if the reaction is the "next" emoji
                waifu_list.append(waifu_list.pop(0))  # Moves the first waifu to the end of the list
                timeout_stamp, navigation_header = await process_reactions(ctx, reaction, waifu_list, navigation_header,
                                                                           listing_message, True, dict_loader_func)

            elif reaction.emoji == PREV_EMOJI and reaction.count > 1:  # Checks if the reaction is the "previous" emoji
                waifu_list.insert(0, waifu_list.pop(-1))  # Moves the last waifu to the start of the list
                timeout_stamp, navigation_header = await process_reactions(ctx, reaction, waifu_list, navigation_header,
                                                                           listing_message, False, dict_loader_func)

            await asyncio.sleep(0.05)

    # Edits the embed to show that the listing is locked when the timeout is reached
    listing_message.embeds[0].set_footer(text=listing_message.embeds[0].footer.text + " 🔒 Locked",
                                         icon_url=listing_message.embeds[0].footer.icon_url)
    await listing_message.edit(embed=listing_message.embeds[0])
