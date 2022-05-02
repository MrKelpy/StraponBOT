# -*- coding: utf-8 -*-
"""
This file is distributed as part of the StraponBOT Project.
The source code may be available for the public at
https://github.com/MrKelpy/StraponBOT

If a license applies for this project, the former can be found
in every distribution, as a "LICENSE" file at top level.
"""

# Built-in Imports
from typing import Optional, List

# Third Party Imports
import discord

# Local Application Imports
from data.globals import bot


async def get_hell_channels():
    """
    Returns a list of the channels with "hell" in their name.
    :return List[discord.TextChannel]: The list with the channels
    """

    hell_channels: Optional[List[discord.TextChannel]] = list()

    for guild in bot.guilds:
        for channel in guild.channels:
            if "hell" in channel.name.lower():
                hell_channels.append(channel)

    return hell_channels


async def get_dead_users():
    """
    Returns a list of the users with a role named "dead"
    :return List[discord.Member]: The list with the users
    """

    dead_users: Optional[List[discord.Member]] = list()

    for guild in bot.guilds:
        for user in guild.members:
            if "dead" in [role.name.lower() for role in user.roles]:
                dead_users.append(user)

    return dead_users


async def purge_hell():
    """
    Clears all of the dead roles from all players and removes all of the "hell" channels
    from the server upon restarts.
    :return None:
    """

    hell_channels: Optional[List[discord.TextChannel]] = await get_hell_channels()
    dead_users: Optional[List[discord.Member]] = await get_dead_users()

    for user in dead_users:
        dead_role: discord.Role = [role for role in user.roles if "dead" in role.name.lower()][0]
        await user.remove_roles(dead_role)

    for channel in hell_channels:
        await channel.delete()
