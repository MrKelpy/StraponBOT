# -*- coding: utf-8 -*-
"""
This module is distributed as part of the Laminaria Core (Python Version).
Get the Source Code in GitHub:
https://github.com/MrKelpy/LaminariaCore

The LaminariaCore is Open Source and distributed under the
MIT License
"""

# Built-in Imports
from typing import Dict, Any, List
from pathlib import Path
import json
import shutil
import os

# Third Party Imports
# Local Application Imports
from .exceptions import InvalidDocumentException


class Document:
    """
    This class represents a Document, UUID named JSON files with
    collection information and json information.
    """

    def __init__(self, path: str, cache: List[Dict[str, Any]]):
        self.path: Path = Path(path)
        self.content: Dict[str, Any] = self.__get_data()
        self.id: str = self.content["_id"]
        self.collection: str = self.content["_collection"]
        self._cache: List[Dict[str, Any]] = cache


    def verify_document(self):
        """
        Verifies the integrity of the document, and if the document
        has been deleted, raise an InvalidDocumentException.
        :return:
        """

        if not os.path.isfile(self.path):
            raise InvalidDocumentException(f"Operation attempted on non-existent document \"{self.id}\"")


    def update(self) -> int:
        """
        Updates the content within the document and removes it from cache.
        :return: int, number of lines affected.
        """
        self.verify_document()
        self.__del_from_cache()

        with open(self.path, "r") as document:  # Registers the document state before the update
            doc_before: List[str] = document.readlines()

        with open(self.path, "w") as document:
            self.content["_id"] = self.id
            self.content["_collection"] = self.collection
            json.dump(self.content, document, indent=4)

        with open(self.path, "r") as document:  # Registers the document state after the update
            doc_after: List[str] = document.readlines()

        return len([line for line in doc_after if line not in doc_before])


    def delete(self):
        """
        Deletes the document from the collection's physical location and
        from cache.
        :return:
        """
        self.verify_document()
        self.__del_from_cache()
        shutil.rmtree(self.path)


    def __get_data(self) -> Dict[str, Any]:
        """
        Returns a dictionary containing all the information present in the document.
        :return:
        """

        with open(self.path, "r") as document:
            data: Dict[str, Any] = json.load(document)
        return data


    def __del_from_cache(self):
        """
        Removes the current document from cache
        :return:
        """

        element: Dict[str, Any] = [cached for cached in self._cache if cached["id"] == self.id][0]
        self._cache.remove(element)
