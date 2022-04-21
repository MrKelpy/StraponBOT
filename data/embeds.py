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

with open("./data/usage_info", "r") as f:
    usage_info: str = f.read()

help_info_embed: discord.Embed = discord.Embed(
    title="How to claim a waifu",
    description=usage_info,
    color=discord.Colour.red()
)

