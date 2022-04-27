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


async def fix_navigation_header(next_page: bool, navigation_header: int, reference: int) -> int:
    """
    Fixes the navigation header accordingly to the given parameters.

    :param bool next_page: Whether the listing should go to the next or prior page
    :param int navigation_header: The navigation header pointing to our current position in the visual list
    :param int reference: The reference page/waifu count to compare the header against

    :return int: The new navigation header
    """

    if next_page: navigation_header += 1
    if navigation_header > reference: navigation_header = 1

    if not next_page: navigation_header -= 1
    if navigation_header < 1: navigation_header = reference

    return navigation_header
