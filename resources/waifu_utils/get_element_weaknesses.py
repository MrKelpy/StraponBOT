# -*- coding: utf-8 -*-
"""
This file is distributed as part of the StraponBOT Project.
The source code may be available at
https://github.com/MrKelpy/StraponBOT

If a license applies for this project, the former can be found
in every distribution, as a "LICENSE" file at top level.
"""

# Built-in Imports
from typing import List

# Third Party Imports
# Local Application Imports
from data.globals import fight_config


async def get_element_weaknesses(target_element: str) -> List[str]:
    """
    Checks the database looping through all elements and returns a list of elements
    that are strong against the specified element

    :param str target_element: The element to check for weaknesses
    :return:
    """

    weaknesses: list = list()
    for element in fight_config["elements"]:

        if target_element in fight_config["elements"][element]["strong_against"]:
            weaknesses.append(element)

    return weaknesses
