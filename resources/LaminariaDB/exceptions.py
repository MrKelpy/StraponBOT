# -*- coding: utf-8 -*-
"""
This module is distributed as part of the Laminaria Core (Python Version).
Get the Source Code in GitHub:
https://github.com/MrKelpy/LaminariaCore

The LaminariaCore is Open Source and distributed under the
MIT License
"""

# Built-in Imports
# Third Party Imports
# Local Application Imports


class CollectionAlreadyExistsException(BaseException):
    """
    Raised when a collection is being created but there's already one with the same name
    """


class InvalidCollectionNameException(BaseException):
    """
    Raised when a collection has an invalid name.
    Collection names only support ASCII characters.
    """


class InvalidCollectionException(BaseException):
    """
    Raised when an operation is attempted on a non-existent collection or when
    an operation is attempted illegally between Collections.
    """


class InvalidDocumentException(BaseException):
    """
    Raised when an operation is attempted on a non-existent Document.
    """