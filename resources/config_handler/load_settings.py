# -*- coding: utf-8 -*-
"""
This file is distributed as part of the <project_name> Project.
The source code may be available at
https://github.com/MrKelpy/<project_name>

If a license applies for this project, the former can be found
in every distribution, as a "LICENSE" file at top level.
"""

# Built-in Imports
from typing import Dict, List
# Third Party Imports
# Local Application Imports


def load_settings(path: str) -> Dict[str, str]:
    """
    Parses the settings config file into a dictionary.
    :param path: String, The path to the config file
    :return: Dict[str, str], the settings dictionary
    """
    with open(path, "r") as config_file:
        settings: List[str] = config_file.readlines()

    # Ignores any "#" or "//" starting lines or any empty strings in the lines.
    filtered_settings: List[str] = [setting.strip() for setting in settings
                         if not setting.startswith("#")
                         and not setting.startswith("//")
                         and setting.strip() != ""]

    # Creates the dictionary by splitting the settings by the "="
    # and assigning the leftmost part to the value, and the rightmost to the key.
    settings_dictionary: Dict[str, str] = dict()
    for setting in filtered_settings:

        key_value_setting: List[str] = setting.split("=")
        settings_dictionary[key_value_setting[0].strip().lower()] = str(key_value_setting[-1].strip())

    return settings_dictionary
