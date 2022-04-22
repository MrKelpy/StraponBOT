# -*- coding: utf-8 -*-
"""
This file is distributed as part of the StraponBOT Project.
The source code may be available at
https://github.com/MrKelpy/StraponBOT

If a license applies for this project, the former can be found
in every distribution, as a "LICENSE" file at top level.
"""

# Built-in Imports
import json
import random

# Third Party Imports
from discord.ext import commands

# Local Application Imports
from data.globals import bot, FAILED_EMOJI, SUCCESS_EMOJI
from resources.waifu_detection.validate_waifu import validate_waifu
from resources.waifu_detection.get_waifu_details import get_waifu_details
from resources.ensure_collection import ensure_collection
from resources.LaminariaDB.Collection import Collection


@bot.command(description="Adapts a mudae waifu to the fighting bot")
async def adapt(ctx: commands.Context):
    """
    Adapts a mudae waifu to the fighting bot. This will convert a given waifu from the mudae bot into an
    usable fighting bot waifu, adding it to the database.
    """

    if not await validate_waifu(ctx):
        await ctx.message.add_reaction(FAILED_EMOJI)
        return

    with open("./data/default_messages.json", "r") as f:
        default_messages = json.load(f)

    waifu_details: dict = await get_waifu_details(ctx)
    waifu_details["owner"] = ctx.author.id
    waifu_details["level"] = 1
    waifu_details["exp"] = 0
    waifu_details["next_level"] = 100
    waifu_details["skill_points"] = random.randint(0, int(waifu_details["kakera_value"]) // 20)
    waifu_details["physical_dmg"] = 1
    waifu_details["magical_dmg"] = 1
    waifu_details["physical_def"] = 1
    waifu_details["magical_def"] = 1
    waifu_details["speed"] = 1
    waifu_details["luck"] = 0
    waifu_details["max_hp"] = 100
    waifu_details["hp"] = 100
    waifu_details["class"] = None
    waifu_details["element"] = random.choice(["Pyro :pyro:", "Hydro :hydro:", "Geo :geo:",
                                              "Anemo :anemo:", "Electro :electro:", "Dendro :dendro",
                                              "Cryo :cryo:"])
    waifu_details["artefacts"] = 0
    waifu_details["messages"] = default_messages
    del waifu_details["kakera_value"]

    waifus_collection: Collection = await ensure_collection(str(ctx.guild.id))
    waifus_collection.insert_one(waifu_details)

    await ctx.message.add_reaction(SUCCESS_EMOJI)
