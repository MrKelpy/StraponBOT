# -*- coding: utf-8 -*-
"""
This file is distributed as part of the <project_name> Project.
The source code may be available at
https://github.com/MrKelpy/<project_name>

If a license applies for this project, the former can be found
in every distribution, as a "LICENSE" file at top level.
"""

# Built-in Imports
# Third Party Imports
from discord.ext import commands

# Local Application Imports
from data.globals import bot, dpyutils


@bot.command(description="Shows this menu.", aliases=("help",))
async def commands(ctx: commands.Context):
    await ctx.message.delete()
    await dpyutils.show_help_menu(ctx)
