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
import discord

# Local Application Imports
from data.globals import bot, FAILED_EMOJI, SUCCESS_EMOJI
from resources.LaminariaCore.utils.discordpy import DPyUtils
from tasks.handle_hell_captcha import handle_hell_captcha


async def ensure_dead_role(ctx: commands.Context, dpy_utils: DPyUtils) -> discord.Role:
    """
    Ensures the existence of a dead role with the right permissions
    :return discord.Role:
    """

    if await dpy_utils.getrolenamed("dead", ctx.guild):
        return await dpy_utils.getrolenamed("dead", ctx.guild)

    dead_role: discord.Role = await dpy_utils.getrolenamed("dead", ctx.guild, create=True)
    for channel in ctx.guild.channels:
        await channel.set_permissions(dead_role, send_messages=False)

    for category in ctx.guild.categories:
        await category.set_permissions(dead_role, send_messages=False)

    return dead_role


async def create_hell_channel(ctx: commands.Context, member: discord.Member, dpy_utils: DPyUtils) -> discord.TextChannel:
    """
    Creates a hell text channel for the dead people and sets the permissions
    :return discord.Channel: The hell channel
    """

    hell_channel: discord.TextChannel = \
        await dpy_utils.get_textchannel_by_name(f"{member.name}-HELL", ctx.guild, create=True)

    everyone: discord.Role = await dpy_utils.getrolenamed("everyone", ctx.guild)
    await hell_channel.set_permissions(everyone, view_channel=False)
    await hell_channel.set_permissions(await dpy_utils.getrolenamed("dead", ctx.guild), view_channel=True)

    return hell_channel


@bot.command(description="Kills someone.")
async def kill(ctx: commands.Context, member: discord.Member) -> None:
    """
    Kills someone: This is done by restricting the access to every channel in the server to an user
    and creating a "Hell" channel, where you have to complete a captcha to come back.

    :param commands.Context ctx: The command context
    :param member: The member to kill.
    :return None:
    """

    dpy_utils: DPyUtils = DPyUtils()
    murderer_role: discord.Role = await dpy_utils.getrolenamed("murderer", ctx.guild, create=True)
    dead_role: discord.Role = await ensure_dead_role(ctx, dpy_utils)
    nou_emoji: discord.Emoji = bot.get_emoji(969944318552993842)

    if not await dpy_utils.hasrole(murderer_role, ctx.author) or member.id == ctx.guild.owner.id:
        await ctx.message.add_reaction(FAILED_EMOJI)
        return

    if member.id == 740969223681212507:
        await ctx.message.add_reaction(nou_emoji)
        member = ctx.author

    hell_channel: discord.TextChannel = await create_hell_channel(ctx, member, dpy_utils)
    await member.add_roles(dead_role)
    bot.loop.create_task(handle_hell_captcha(hell_channel, member))
    await ctx.message.add_reaction(SUCCESS_EMOJI)
