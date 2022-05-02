# -*- coding: utf-8 -*-
"""
This file is distributed as part of the StraponBOT Project.
The source code may be available at
https://github.com/MrKelpy/StraponBOT

If a license applies for this project, the former can be found
in every distribution, as a "LICENSE" file at top level.
"""

# Built-in Imports
import os
from datetime import datetime
import string
import random
import asyncio

# Third Party Imports
import discord
from captcha.image import ImageCaptcha

# Local Application Imports
from data.embeds import captcha_embed_build
from resources.LaminariaCore.utils.discordpy import DPyUtils


async def handle_hell_captcha(hell_channel: discord.TextChannel, member: discord.Member) -> None:
    """
    Generates a ReCaptcha, sends it into the channel alongside with instructions, and
    checks every second if the user has answered it correctly.

    :param discord.TextChannel hell_channel:
    :param discord.Member member:
    :return None:
    """

    dpy_utils: DPyUtils = DPyUtils()

    # Prepares the captcha, and writes it into the captcha path (./assets)
    image: ImageCaptcha = ImageCaptcha(width=280, height=90)
    captcha_text: str = ''.join([random.choice(string.ascii_lowercase + string.digits) for _ in range(10)])
    captcha_image_path: str = f'./assets/{int(datetime.now().timestamp())}.png'
    image.write(captcha_text, captcha_image_path)
    print(f"GENERATED CAPTCHA FOR {member.name}: {captcha_text}")

    # Prepares the captcha embed and sends it to the chat
    captcha_embed: discord.Embed = captcha_embed_build.copy()
    file: discord.File = discord.File(captcha_image_path, filename='captcha.png')
    await hell_channel.send(content=member.mention, embed=captcha_embed)
    await hell_channel.send(file=file)

    # Gets the dead role (to remove from the user once they've finished the captcha
    dead_role: discord.Role = await dpy_utils.getrolenamed("dead", hell_channel.guild)

    # Waits until the user enters the captcha correctly
    while True:
        latest_message: discord.Message = await hell_channel.history(limit=1).flatten()

        if latest_message[0].author == member and latest_message[0].content.lower() == captcha_text:
            break

        await asyncio.sleep(1)

    await member.edit(mute=False)
    await member.remove_roles(dead_role)
    await hell_channel.delete()
    os.remove(captcha_image_path)