# -*- coding: utf-8 -*-
"""
This module is distributed as part of the Laminaria Core (Python Version).
Get the Source Code in GitHub:
https://github.com/MrKelpy/LaminariaCore

The LaminariaCore is Open Source and distributed under the
MIT License
"""

# Built-in Imports
import os
import random
from datetime import datetime

# Third Party Imports
import interactions
from fpdf import FPDF

# Local Application Imports


class InteractionUtils:
    """
    This class implements useful functions to for usage whilst making discord bots.
    All fot the methods in here are async methods, meaning they cannot be run from anywhere
    but async functions.
    This class uses discord-py-interactions.
    """

    def __init__(self, bot: interactions.Client):
        # Properties
        self.bot = bot

        # Aliases
        self.tc = self.twochars


    async def hasrole(self, role: interactions.Role, user: interactions.Member, add: bool = False):
        """
        Checks if a user has a certain role.
        :param role: The role to be checked for. -> interactions.Role
        :param user: The user. -> interactions.Member
        :param add: If set to True, adds the role to the user, will always return True.
        :return: True, if user has the role. False otherwise.
        """

        for r in user.roles:

            if r == role:
                return True

        else:
            if add is True:
                await self.bot.http.add_member_role()
                return True

            return False


    # noinspection PyTypeChecker
    async def send_loading(self, channel_id: int, color: int = int("eb4034", 16)):
        """
        Sends a loading embed to a specified channel.
        :param channel_id: The channel for the message to be sent to. -> discord.TextChannel
        :param color: The embed color. -> int
        :return: interactions.Embed
        """

        loading_embed = interactions.Embed(
            title='Loading...',
            color=color
        )

        channel = interactions.Channel(**await self.bot.http.get_channel(channel_id), _client=self.bot.http)
        loading = await channel.send(embeds=loading_embed)
        return loading


    async def get_textchannel_firstmessage(self, channel_id: int):
        """
        Returns the first message on a TextChannel
        :param channel_id: The textchannel to retrieve the message from. -> discord.TextChannel
        :return: interactions.Message
        """

        channel = interactions.Channel(**await self.bot.http.get_channel(channel_id), _client=self.bot.http)
        all_messages = await self.bot.http.get_channel_messages(channel)
        all_messages.reverse()

        return all_messages[0]


    async def show_help_menu(self, ctx: interactions.CommandContext, color: int = int("eb4034", 16),
                             reverse: int = False, testing: bool = False):
        """
        Standard help menu used between bots created by Alex, with loads of quirks to make the UI more appealing.
        The help menu is completely computer-generated.

        Description management:
            > Leaving the description of a command without text will it not be shown in the UI
            > Writing |String| at the beggining of a command description will have it sorted into a category
            (Replace "String" with the category name)
            > Categories are sorted alphabetically, aswell as bot_commands.
            > Not specifying a category will result in the command being thrown into a "General" category

        :param testing: If set to true, processes all commands from all scopes
        :param reverse:
        :param ctx: discord context.
        :param color: Help menu embed color
        :return: discord.Embed
        """

        help_menu_base = interactions.Embed(
            title=f"{self.bot.me.name}'s Help Menu - ",
            color=color
        )

        dev = await self.bot.http.get_user(740969223681212507)
        commands_dictionary = dict()
        embed_list = list()

        # Checks for the testing mode
        if testing:
            scope = 930131186930565130
        else:
            scope = None

        for command in self.bot.http.get_application_command(self.bot.me.id, guild_id=scope):
            # Iterates through all the registered bot_commands

            if not command["description"]:
                # Skips over the command if no description is provided
                continue

            category_name = "General"
            if command["description"].startswith("|") and command["description"].count(
                    "|") == 2 and not command.description.endswith("||"):
                # Parses out the category of a command if a match is detected

                category_name = command["description"].split("|")[1].strip().title()
                command.description = command["description"].split("|")[2].strip()

            params = ""
            alias_list = "No aliases found"
            for param in command.clean_params:
                # Parses out the command parameters for usage in the command info
                params += f" <{param}> "

            if command.aliases:
                # If any command aliases exist, parse them out for usage in the command info
                alias_list = ""

                for alias in command.aliases:
                    alias_list += f"|/{alias}| "

            # Build the dict update
            try:
                _ = commands_dictionary[category_name]
                commands_dictionary[category_name].append([command.name, command.description, alias_list, params])

            except KeyError:
                command_registration = {category_name: [[command.name, command.description, alias_list, params]]}
                commands_dictionary.update(command_registration)

        for category in sorted(commands_dictionary):
            # Loads in the categories with their bot_commands to the help menu

            help_menu_base.title = f"{self.bot.me.name}'s Help Menu - {category} Commands"

            for command in sorted(commands_dictionary[category]):
                # Gets the command info
                name = command[0]
                description = command[1]
                aliases = command[2]
                params = command[3]

                help_menu_base.fields.append(interactions.EmbedField(name=name.title(),
                                                                     value=f"{description}\n`USAGE: /{name}{params}`\n"
                                                                           f"`ALIASES: {aliases}`", inline=False))
                help_menu_base.timestamp = datetime.now()
                help_menu_base.footer = f"Developed by {dev}"
                help_menu_base.thumbnail = self.bot.me.icon

            embed_list.append(help_menu_base)

        if reverse:
            embed_list = reversed(embed_list)

        for embed in embed_list:
            # Sends all the embeds in the list
            await ctx.send(embeds=embed)


    @staticmethod
    async def getrolenamed(role: str, guild: interactions.Guild, create: bool = False, exact: bool = True):
        """
        Returns a role inside a Guild based on a given name.
        :param role: The role to be gathered. -> str
        :param guild: The guild to retrieve the role from. -> interactions.Guild
        :param create: If set to True, creates the role. (If non existant!)
        :param exact: If set to True, matches the role exactly
        :return: discord.Role, None if not found.
        """

        for r in guild.roles:

            if exact and r.name == role:
                return r

            elif role in r.name:
                return r

        else:
            if create is True:
                random_color = "%02x%02x%02x" % (
                    random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                return_role = await guild.create_role(name=role, color=int(random_color, 16))
                return return_role

            return None


    @staticmethod
    async def get_textchannel_by_name(channel: str, guild: interactions.Guild,
                                      delete: bool = False, create: bool = False, category: int = None,
                                      exact: bool = True):
        """
        Returns a text channel based on a given name.
        :param channel: The channel to be gathered. -> str
        :param guild: The guild to retrieve the channel from. -> interactions.Guild
        :param delete: If set to True, deletes the role. (If found!)
        :param create: If set to True, creates the role. (If not found!)
        :param category: The category ID to create the channel into. (If create is True!)
        :param exact: If set to True, the channelname needs to match the channel at 100%. Else, no.
        :return: interactions.Channel, None if not found.
        """

        for text_channel in [x for x in guild.channels if x.type == interactions.ChannelType.GUILD_TEXT]:

            if exact:
                if text_channel.name == channel.lower():

                    if delete is True:
                        await text_channel.delete()
                        continue
                    return text_channel

            else:
                if channel.lower() in text_channel.name:

                    if delete is True:
                        await text_channel.delete()
                        continue
                    return text_channel

        if create is True:
            text_channel = await guild.create_channel(name=channel, parent_id=category,
                                                      type=interactions.ChannelType.GUILD_TEXT)
            return text_channel

        return None


    @staticmethod
    async def get_category_by_name(category_name: str, guild: interactions.Guild, delete: bool = False,
                                   create: bool = False,
                                   exact: bool = True):
        """
        Returns a category based on a given name.
        :param exact: If set to True, matches the name exactly as it is.*
        :param category_name: The category to be gathered. -> str
        :param guild: The guild to retrieve the category from. -> interactions.Guild
        :param delete: If set to True, deletes the category. (If found!)
        :param create: If set to True, creates the category. (If not found!)
        :return: interactions.Channel, None if not found.
        """

        for category in [x for x in guild.channels if x.type == interactions.ChannelType.GUILD_CATEGORY]:

            if exact and category.name == category_name:

                if delete is True:
                    await category.delete()
                    continue
                return category

            elif not exact and category_name in category.name:

                if delete is True:
                    await category.delete()
                    continue
                return category

        if create is True:
            category = await guild.create_channel(name=category_name, type=interactions.ChannelType.GUILD_CATEGORY)
            return category

        return None


    @staticmethod
    async def twochars(arg):
        """
        Formats a string of two characters into the format of (0X), useful for date formatting.
        :param arg: The string
        :return: String
        """

        return "%02d" % arg


    async def get_formatted_date_now(self, include_seconds: bool = False, formatting: int = 1):
        """
        Returns the current date in the handy DD/MM/YY - HH:MM:SS format (default) or in the specified one.
        :param formatting: Format type -> int
        :param include_seconds: If set to True, include seconds in the format.
        :return: String
        """

        now = datetime.now()
        if formatting == 1:
            date_string = f"{await self.tc(str(now.day))}/{await self.tc(str(now.month))}/{await self.tc(str(now.year))} - " \
                          f"{await self.tc(str(now.hour))}:{await self.tc(str(now.minute))}"

        elif formatting == 2:
            date_string = f"{await self.tc(str(now.day))}.{await self.tc(str(now.month))}.{await self.tc(str(now.year))}_" \
                          f"{await self.tc(str(now.hour))}.{await self.tc(str(now.minute))}"

        else:
            date_string = f"{await self.tc(str(now.day))}/{await self.tc(str(now.month))}/{await self.tc(str(now.year))} - " \
                          f"{await self.tc(str(now.hour))}:{await self.tc(str(now.minute))}"

        if include_seconds:
            date_string += f":{await self.tc(str(now.second))}"

        return date_string


    async def get_formatted_date(self, date: datetime, include_seconds: bool = False):
        """
        Returns a given date in the handy DD/MM/YY - HH:MM:SS format.
        :param date: The date to be formatted -> datetime.datetime
        :param include_seconds: If set to True, include seconds in the format.
        :return: String
        """

        date_string = f"{await self.tc(str(date.day))}/{await self.tc(str(date.month))}/{await self.tc(str(date.year))} - " \
                      f"{await self.tc(str(date.hour))}:{await self.tc(str(date.minute))}"

        if include_seconds:
            date_string += f":{await self.tc(str(date.second))}"

        return date_string


    @staticmethod
    async def get_member_object(member_id: int, guild: interactions.Guild):
        """
        Returns a discord.Member object of a member from a given ID
        :param member_id: The member ID. -> int
        :param guild: The guild to retrieve the member from. -> discord.Guild
        :return: discord.Member, None if not found.
        """

        for member in guild.members:

            if int(member.id) == int(member_id):
                return member

        return None


    @staticmethod
    async def convert_txt_to_pdf(path: str):
        """
        Converts a .txt file to a .pdf file
        :param path: The path for the file. -> str
        :return:
        """

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=15)
        output_path = str(os.path.splitext(path)[0]) + ".pdf"

        with open(path, 'r') as txtfile:
            lines = txtfile.readlines()

        for line in lines:

            if line == '\n':
                pdf.cell(200, 10, txt='\n', ln=1, align="L")
                continue

            if line[0] == "|" and line[2] == "|":
                pdf.cell(200, 10, txt=line[3:].strip(), ln=1, align=line[1])
                continue

            pdf.cell(200, 10, txt=line.strip(), ln=1, align="L")

        pdf.output(output_path)


    @staticmethod
    async def load_missing_perms_embed(color:int = int("eb4034", 16)):
        """
        Quickly loads a missing permissions embed
        :param color: The embed color
        :return: discord.Embed
        """

        embed = interactions.Embed(
            title="Missing permissions!",
            description="Sorry, you can't use this command.",
            color=color
        )
        embed.timestamp = datetime.now()
        return embed
