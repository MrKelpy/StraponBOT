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
from datetime import datetime

# Third Party Imports
from discord.ext import commands
import discord
import asyncio

# Local Application Imports
from resources.LaminariaDB.Document import Document
from data.embeds import waifu_listing_embed_build
from data.globals import NEXT_EMOJI, PREV_EMOJI, fight_config


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


async def load_listing_index(ctx: commands.Context, waifu_list: List[Document],
                             index: int, navigation_header: int) -> discord.Embed:
    """
    Loads the embed for the specified
    :param commands.Context ctx: The command context
    :param List[Document] waifu_list: The list of waifus belonging to the user
    :param int index: The index in the list to load the waifu embed for
    :param int navigation_header: A header to determine the current position in the apparent list we are in.
    :return discord.Embed: The embed for the waifu at the specified index
    """

    element_name: str = waifu_list[index].content["element"]
    element_icon: str = fight_config["elements"][element_name]["emoji"]
    waifu_listing_embed: discord.Embed = waifu_listing_embed_build.copy()
    waifu_listing_embed.title = waifu_list[index].content["name"]
    waifu_listing_embed.description = f"{waifu_list[index].content['source']} :{waifu_list[index].content['gender']}_sign:\n"
    waifu_listing_embed.description += f"LEVEL: {waifu_list[index].content['level']} " \
                                             f"({waifu_list[index].content['exp']}/{waifu_list[index].content['next_level']})\n"
    waifu_listing_embed.description += f"CLASS: {waifu_list[index].content['class']} | " \
                                       f"{element_name} {element_icon}\n"
    waifu_listing_embed.description += f"SKILL POINTS: {waifu_list[index].content['skill_points']}\n"
    waifu_listing_embed.description += f"HP: {waifu_list[index].content['max_hp']}"
    waifu_listing_embed.add_field(name="Physical Damage", value=waifu_list[index].content["physical_dmg"], inline=True)
    waifu_listing_embed.add_field(name="Magical Damage", value=waifu_list[index].content["magical_dmg"], inline=True)
    waifu_listing_embed.add_field(name="Physical Defense", value=waifu_list[index].content["physical_def"], inline=True)
    waifu_listing_embed.add_field(name="Magical Damage", value=waifu_list[index].content["magical_def"], inline=True)
    waifu_listing_embed.add_field(name="Speed", value=waifu_list[index].content["speed"], inline=True)
    waifu_listing_embed.add_field(name="Luck", value=waifu_list[index].content["luck"], inline=True)
    waifu_listing_embed.set_footer(text=f"Belongs to {ctx.author.name} -- {navigation_header}/{len(waifu_list)}",
                                   icon_url=ctx.author.avatar_url)
    waifu_listing_embed.set_image(url=waifu_list[index].content["image"])
    waifu_listing_embed.colour = waifu_list[index].content["embed_colour"]

    return waifu_listing_embed
    

async def handle_waifu_listing(ctx: commands.Context, waifu_list: List[Document],
                               listing_message: discord.Message, starting_index: int):
    """
    Handles the listing of an user's waifus. This function will listen for any reactions added to the message
    every .05 seconds, and show the next/prior waifu in the list accordingly to the reaction. The waifus will be
    shown alongside all their stats. The listing will stop working after a timeout of 30s.

    :param discord.Message listing_message: The message to be edited with the waifus
    :param commands.Context ctx: The command context
    :param List[Document] waifu_list: A list of documents from the database containing all of the waifus for the user.
    :param int starting_index: The index of the waifu to start the listing with.
    :return None:
    """

    timeout_stamp: float = datetime.now().timestamp() + 30.0
    navigation_header: int = starting_index+1
    first_waifu: discord.Embed = await load_listing_index(ctx, waifu_list, starting_index, navigation_header)
    await listing_message.edit(embed=first_waifu)  # Edits the embed with a waifu from the starting index to display
    await listing_message.add_reaction(PREV_EMOJI)
    await listing_message.add_reaction(NEXT_EMOJI)

    # Listens for any reactions added to the message every .05 seconds
    while datetime.now().timestamp() <= timeout_stamp:
        for reaction in listing_message.reactions:

            if reaction.emoji == NEXT_EMOJI and reaction.count > 1:  # Checks if the reaction is the "next" emoji
                waifu_list.append(waifu_list.pop(0))  # Moves the first waifu to the end of the list
                navigation_header = await update_header(waifu_list, True, navigation_header)  # Updates the navigation header

                async for user in reaction.users():  # Removes the reaction from every user but the bot
                    if user.id == 966370729597730966: continue
                    await listing_message.remove_reaction(NEXT_EMOJI, user)

                await listing_message.edit(embed=await load_listing_index(ctx, waifu_list, 0, navigation_header))
                timeout_stamp = datetime.now().timestamp() + 30.0  # Resets the timeout

            elif reaction.emoji == PREV_EMOJI and reaction.count > 1:  # Checks if the reaction is the "previous" emoji
                waifu_list.insert(0, waifu_list.pop(-1))  # Moves the last waifu to the beginning of the list
                navigation_header = await update_header(waifu_list, False, navigation_header)  # Updates the navigation header

                async for user in reaction.users():  # Removes the reaction from every user but the bot
                    if user.id == 966370729597730966: continue
                    await listing_message.remove_reaction(PREV_EMOJI, user)

                await listing_message.edit(embed=await load_listing_index(ctx, waifu_list, 0, navigation_header))
                timeout_stamp = datetime.now().timestamp() + 30.0  # Resets the timeout

            await asyncio.sleep(0.05)

    # Edits the embed to show that the listing is locked when the timeout is reached
    listing_message.embeds[0].set_footer(text=listing_message.embeds[0].footer.text + " 🔒 Locked",
                                         icon_url=listing_message.embeds[0].footer.icon_url)
    await listing_message.edit(embed=listing_message.embeds[0])
