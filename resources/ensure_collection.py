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
from resources.LaminariaDB.LaminariaDB import LaminariaDB
from resources.LaminariaDB.Collection import Collection


async def ensure_collection(collection_name: str) -> Collection:
    """
    Ensures that the given collection exists inside the database
    :param str collection_name: The name of the collection to ensure the existence of
    :return Collection: The collection object that was ensured
    """

    if collection_name not in LaminariaDB("./databases").collections:
        return LaminariaDB("./databases").add_collection(collection_name)

    return LaminariaDB("./databases").collections[collection_name]
