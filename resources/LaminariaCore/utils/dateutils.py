# -*- coding: utf-8 -*-
"""
This module is distributed as part of the Laminaria Core (Python Version).
Get the Source Code in GitHub:
https://github.com/MrKelpy/LaminariaCore

The LaminariaCore is Open Source and distributed under the
MIT License
"""

# Built-in Imports
import datetime

# Third Party Imports
# Local Application Imports


def twochars(arg):
    """
    Formats a string of two characters into the format of (0X), useful for date formatting.
    :param arg: The string
    :return: String
    """

    if len(arg) == 1:
        return f"0{arg}"
    return arg


def get_formatted_date(date: datetime, include_seconds: bool = False):
    """
    Returns a given date in the handy DD/MM/YY - HH:MM:SS format.
    :param date: The date to be formatted -> datetime.datetime
    :param include_seconds: If set to True, include seconds in the format.
    :return: String
    """

    date_string = f"{twochars(str(date.day))}/{twochars(str(date.month))}/{twochars(str(date.year))} - " \
                  f"{twochars(str(date.hour))}:{twochars(str(date.minute))}"

    if include_seconds:
        date_string += f":{twochars(str(date.second))}"

    return date_string


def get_formatted_date_now(include_seconds: bool = False, formatting: int = 1):
    """
    Returns the current date in the handy DD/MM/YY - HH:MM:SS format (default) or in the specified one.
    :param formatting: Format type -> int
    :param include_seconds: If set to True, include seconds in the format.
    :return: String
    """

    now = datetime.datetime.now()
    if formatting == 1:
        date_string = f"{twochars(str(now.day))}/{twochars(str(now.month))}/{twochars(str(now.year))} - " \
                      f"{twochars(str(now.hour))}:{twochars(str(now.minute))}"

    elif formatting == 2:
        date_string = f"{twochars(str(now.day))}.{twochars(str(now.month))}.{twochars(str(now.year))}_" \
                      f"{twochars(str(now.hour))}.{twochars(str(now.minute))}"

    else:
        date_string = f"{twochars(str(now.day))}/{twochars(str(now.month))}/{twochars(str(now.year))} - " \
                      f"{twochars(str(now.hour))}:{twochars(str(now.minute))}"

    if include_seconds:
        date_string += f":{twochars(str(now.second))}"

    return date_string


def time_until_midnight():
    """
    Get seconds left until midnight
    """
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    timedelta_until_midnight = datetime.datetime.combine(tomorrow, datetime.time.min) - datetime.datetime.now()
    return timedelta_until_midnight.seconds
