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

# Third Party Imports
from discord.ext import commands
import discord

# Local Application Imports
from data.globals import bot, FAILED_EMOJI, SUCCESS_EMOJI
from resources.LaminariaDB.Collection import Collection
from resources.LaminariaDB.Document import Document
from resources.ensure_collection import ensure_collection
from resources.waifu_utils.validate_basics import validate_basics


async def parse_skill_field(field: str) -> str:
    """
    Returns the key for the specified field. This function aims to
    guess at which field the user wants to add the skillpoints to.
    :param str field: The field to guess where to add the skillpoints to.
    :return str: The key for the field.
    """

    fields: Dict[str, List[str]] = {
        "physical_dmg": ["physical", "physical damage", "physical dmg", "pd", "dmg", "damage"],
        "magical_dmg": ["magical", "magical damage", "magical dmg", "md", "magic", "magic damage"],
        "physical_def": ["physical defense", "physical def", "def", "defense"],
        "magical_def": ["magical defense", "magical def", "magic def", "magic defense"],
        "speed": ["speed", "spd", "vroom"],
        "luck": ["luck", "treasure"],
     }

    for key, values in fields.items():
        if field.lower() in values:
            return key


@bot.command(description="|WAIFU| Adds a given amount of skill points to a character")
async def addskill(ctx: commands.Context, amount: int, *, field: str) -> None:
    """
    Adds X amount of skillpoints to a given field for the waifu the user is replying to.
    The reference waifu must be owned by the user.

    :param commands.Context ctx: The context of the command.
    :param int amount: The amount of skillpoints to add.
    :param str field: The field to add the skillpoints to.
    :return None:
    """

    if ctx.message.reference:
        waifu_message: discord.Message = await ctx.channel.fetch_message(ctx.message.reference.message_id)

    else:
        waifu_message: List[discord.Message] = await ctx.channel.history(limit=2).flatten()
        waifu_message: discord.Message = waifu_message[-1]

    if not await validate_basics(ctx, waifu_message):
        return await ctx.message.add_reaction(FAILED_EMOJI)

    collection: Collection = await ensure_collection(str(ctx.guild.id))
    waifu_name: str = waifu_message.embeds[0].author.name if waifu_message.embeds[0].author.name \
                      else waifu_message.embeds[0].title
    waifu_document: Document = collection.find(query={"name": waifu_name.lower()},
                                               limit=1)[0]

    if amount > waifu_document.content["skill_points"]:
        return await ctx.message.add_reaction(FAILED_EMOJI)

    field = await parse_skill_field(field)
    waifu_document.content[field] += amount
    waifu_document.content["skill_points"] -= amount
    waifu_document.update()
    await ctx.message.add_reaction(SUCCESS_EMOJI)
