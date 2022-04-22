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
# Local Application Imports
from data.globals import bot
from data.globals import settings


@bot.command(description="Get an invite link for the bot.")
async def invite(ctx):
    """
    Get an invite link for the bot.
    """
    await ctx.send(f"https://discord.com/api/oauth2/authorize?client_id=966370729597730966&permissions=8&scope=bot")
