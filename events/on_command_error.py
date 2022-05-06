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
from discord.ext import commands

# Local Application Imports
from data.globals import bot, FAILED_EMOJI


@bot.event
async def on_command_error(ctx: commands.Context, error):
    """
    Generally handles any errors that might happen.
    :param commands.Context ctx: The error context
    :param commands.errors.* error: The error that occurred
    :return None:
    """

    # Ignores the command not found errors.
    if isinstance(error, commands.CommandNotFound):
        return

    if isinstance(error, commands.MissingRequiredArgument):
        return await ctx.message.add_reaction(FAILED_EMOJI)

    raise error
