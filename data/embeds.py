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
from data.globals import usage_info

help_info_embed: discord.Embed = discord.Embed(
    title="",
    description=usage_info,
    color=discord.Colour.red()
)


waifu_listing_embed_build: discord.Embed = discord.Embed(
)


captcha_embed_build: discord.Embed() = discord.Embed(
    title="Congratulations! You have been killed!",
    description="Why? How? What? Who? Haha! Well then, you managed to be so god damn annoying that someone ended up "
                "killing you! How nice! Now, if you want to go back, solve this captcha!",
    color=discord.Colour.dark_red()
)
