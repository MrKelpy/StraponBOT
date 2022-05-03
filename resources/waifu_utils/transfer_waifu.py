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
from resources.LaminariaDB.Document import Document


async def transfer_waifu(waifu: Document, user: int) -> None:
    """
    Transfers the waifu from an user to the other.
    :param Document waifu: The waifu target
    :param int user: The user ID
    :return None:
    """

    waifu.content["owner"] = user
    waifu.update()
