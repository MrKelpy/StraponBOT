# -*- coding: utf-8 -*-
"""
This module is distributed as part of the Laminaria Core (Python Version).
Get the Source Code in GitHub:
https://github.com/MrKelpy/LaminariaCore

The LaminariaCore is Open Source and distributed under the
MIT License
"""

# Built-in Imports
from typing import Dict, List, Any
from pathlib import Path
import string
import os

# Third Party Imports
# Local Application Imports
from .exceptions import *
from .Collection import Collection


class LaminariaDB:
    """
    Main class for the implementation of the Laminaria Database.
    This is the only class that needs to ever be called at any point.
    """

    def __init__(self, path: str):
        self._path: Path = Path(path)
        self._cache: List[Dict[str, Any]] = list()
        self.name: str = self._path.name
        self.__ensure_database()
        self.collections: Dict[str, Collection] = self.__get_collections()


    def add_collection(self, name: str) -> Collection:
        """
        Creates a collection inside the database.

        A collection is a portion of the database that contains
        JSON documents with data with the aim of organising them
        in a structured and clear way.

        Two collections with the same name can't exist, and collection
        names can only contain ASCII characters.
        :return: Collection, new collection.
        """

        if name in os.listdir(self._path):
            raise CollectionAlreadyExistsException(f"A collection named \"{name}\" already exists.")

        # Checks if any x isn't present in the allowed characters for each letter in the name.
        allowed_characters: str = string.ascii_letters + string.digits
        if any(x not in allowed_characters for x in name):
            raise InvalidCollectionNameException("Non-ASCII characters cannot be used to name collections.")

        # Creates the new collection directory
        collection_path: str = os.path.join(self._path, name)
        os.makedirs(collection_path)

        # Adds the new collection to the collections attribute and returns it
        newcoll: Collection = Collection(collection_path, self._cache)
        self.collections[name] = Collection(collection_path, self._cache)
        return newcoll


    def __ensure_database(self):
        """
        Ensures that the specified folder for the database exists.
        :return:
        """

        if not os.path.isdir(self._path):
            os.makedirs(self._path)


    def __get_collections(self) -> Dict[str, Collection]:
        """
        Returns all the collections registered in the database.
        :return: Dict[str, Collection], a dictionary containing a key:val association for the collections.
        """
        collection_dict: Dict[str, Collection] = dict()

        for collectdir in os.listdir(self._path):
            collection_path: str = os.path.join(self._path, collectdir)
            collection_dict[collectdir] = Collection(collection_path, self._cache)

        return collection_dict
