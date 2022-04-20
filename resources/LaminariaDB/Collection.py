# -*- coding: utf-8 -*-
"""
This module is distributed as part of the Laminaria Core (Python Version).
Get the Source Code in GitHub:
https://github.com/MrKelpy/LaminariaCore

The LaminariaCore is Open Source and distributed under the
MIT License
"""

# Built-in Imports
from pathlib import Path
from typing import Dict, Any, List
import os
import uuid
import shutil
import json

# Third Party Imports
# Local Application Imports
from .exceptions import InvalidCollectionException
from .Document import Document


class Collection:
    """
    This class represents a collection, used indirectly by the programmer and
    interacts with documents.
    This class is not directly aware of the LaminariaDB class.
    """

    def __init__(self, path: str, cache: List[Dict[str, Any]]):
        self.path: Path = Path(path)
        self.name: str = self.path.name
        self._cache: List[Dict[str, Any]] = cache


    def verify_collection(self):
        """
        Verifies the integrity of the collection, and if the collection
        has been dropped, raise an InvalidCollectionException.
        :return:
        """

        if not os.path.isdir(self.path):
            raise InvalidCollectionException(f"Operation attempted on dropped collection \"{self.name}\"")


    def drop(self) -> int:
        """
        Deletes the collection from the database's physical location and cache.
        All the contents inside the collection will also be deleted from the former.
        :return: int, amount of files affected.
        """
        self.verify_collection()
        affected = len(os.listdir(self.path))
        shutil.rmtree(self.path)
        self.__drop_cache()
        return affected


    def find(self, query: Dict[str, Any] = None, limit: int = None) -> List[Document]:
        """
        Returns all the Documents with information that matches the query.
        :param limit: The limit of matches to be returned.
        :param query: The information pattern to match the documents with.
        :return: List[Document], a list of the matched documents.
        """
        self.verify_collection()
        matches: List[Document] = self.__find_in_cache(query=query, limit=limit)

        for index, docfile in enumerate(os.listdir(self.path)):

            if len(matches) == limit: break  # Breaks when the limit is reached

            # Prevents document match duplication with elements added from cache
            if any(item for item in matches if item.id == docfile[:-5]): continue

            filepath = os.path.join(self.path, docfile)
            with open(filepath, "r") as document:
                docinfo: Dict[str, Any] = json.load(document)


            # For each key in the query dict keys, check if the key:val in docinfo exists.
            # Also appends all the matches to cache
            if query is None or all(key in docinfo and docinfo[key] == query[key] for key in query):
                doc = Document(filepath, self._cache)
                matches.append(doc)
                self._cache.append({"id": doc.id, "collection": self.name, "document": doc})

        return matches


    def merge(self, collection: object) -> int:
        """
        Merges a collection with another collection.
        All the files in the current collection will be sent over to the other one,
        and the current collection will be dropped.
        :return: int, amount of files affected.
        """
        self.verify_collection()

        if type(collection) != type(self):  # Ensures that only Collection objects are passed in.
            raise TypeError(f"Invalid object type \"{type(collection)}\" for merging with a Collection.")
        collection: Collection  # Correctly typehints the collection parameter

        if collection.__hash__() == self.__hash__():  # Ensures that a collection can't merge with itself.
            raise InvalidCollectionException(f"Illegal merge with collections -> {self} && {collection}")

        # Moves all files from a collection to the other
        documents_list = self.find()
        for document in documents_list:
            destination: str = os.path.join(collection.path, document.id + ".json")
            shutil.move(document.path, destination)

        self.drop()  # Drops self because the current collection has now merged with another
        return len(documents_list)


    def insert_one(self, data: dict):
        """
        Inserts a single document into the collection.
        This action will create a JSON document into
        :param data: The dictionary to dump into the document.
        :return:
        """
        self.verify_collection()

        file_uuid: str = str(uuid.uuid4())
        filepath: str = os.path.join(self.path, file_uuid + ".json")

        with open(filepath, "w") as document:

            data["_id"] = file_uuid
            data["_collection"] = self.name

            json.dump(data, document, indent=4)


    def insert_many(self, *data: dict):
        """
        Inserts a single document into the collection.
        This action will create a JSON document into
        :param data: A varargs list of dictionaries to be dumped into the many Documents
        :return:
        """
        self.verify_collection()

        for serializable in data:

            file_uuid: str = str(uuid.uuid4())
            filepath: str = os.path.join(self.path, file_uuid + ".json")

            with open(filepath, "w") as document:

                serializable["_id"] = file_uuid
                serializable["_collection"] = self.name

                json.dump(serializable, document, indent=4)


    def __find_in_cache(self, query: Dict[str, Any] = None, limit: int = None) -> List[Document]:
        """
        Goes through the cache and matches the query to any of the cached documents.
        This is way faster than using self.find(), which is why it will always run first
        to improve speed.
        This function respects the limits and query of the original find() call.
        :return: List[Documents], a list of the cached documents found.
        """
        matches: List[Document] = list()

        # Returns an empty list incase the cache is empty
        if not self._cache:
            return matches

        for cached in self._cache:
            if len(matches) == limit: break
            docinfo: Dict[str, Any] = cached["document"].content

            # For each key in the query dict keys, check if the key:val in docinfo exist.
            if query is None or all(key in docinfo and docinfo[key] == query[key] for key in query):
                matches.append(cached["document"])

        return matches


    def __drop_cache(self):
        """
        Deletes all the documents in cache for the current Collection.
        :return:
        """

        _destroy = [cached for cached in self._cache if cached["collection"] == self.name]

        for element in _destroy:
            self._cache.remove(element)
