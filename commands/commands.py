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
from discord.ext import commands

# Local Application Imports
from data.globals import bot, dpyutils
from data.embeds import help_info_embed


@bot.command(description="Shows this menu.", aliases=("help",))
async def commands(ctx: commands.Context):
    await ctx.message.delete()
    await dpyutils.show_help_menu(ctx, colour=discord.Colour.blue())
    await ctx.send(embed=help_info_embed)
