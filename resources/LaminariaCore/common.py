# -*- coding: utf-8 -*-
"""
This file is distributed as part of the PythonLC Project.
The source code may be available for the public at
https://github.com/MrKelpy/PythonLC

If a license applies for this project, the former can be found
in every distribution, as a "LICENSE" file at top level.
"""

# Built-in Imports
# Third Party Imports
import screeninfo

# Local Application Imports


def get_absolute_screen_coords(relx, rely):
    """
    Returns absolute screen coordinates based off the given relative
    coordinates. For instance, in a 1920x720 screen, the x50, y50 input would be
    x960, y360.
    :param relx: Relative X Coordinate
    :param rely: Relative Y Coordinate
    :return: Absolute Coordinates
    """

    monitor = screeninfo.get_monitors()[0]
    x = (relx * monitor.width) / 100
    y = (rely * monitor.height) / 100
    return x, y


def get_relative_screen_coords(x, y):
    """
    Returns relative screen coordinates based off the given absolute
    coordinates. The relative coordinates are percentage-based values calculates
    relatively to the monitor specs and the given coords.
    :param x: Absolute X
    :param y: Absolute Y
    :return:
    """

    monitor = screeninfo.get_monitors()[0]
    relx = (x * 100) / monitor.width
    rely = (y * 100) / monitor.height
    return relx, rely