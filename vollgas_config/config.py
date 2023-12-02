#!/usr/bin/env python
"""Shared functions and tools.

Copyright (c) 2020 Christopher Kauffman

Attributes:
    None

Todo:
    * None

.. Black Coding Style:
   https://github.com/python/black

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

.. _Example Google Style Python Docstrings
   http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""
from collections import UserDict
import json
import logging
import os.path

import jsonschema
import mergedeep
import yaml

logger = logging.getLogger(__name__)


# pylint: disable=too-few-public-methods
class Config(UserDict):
    """Config Class

    Loads config data from json or yaml to a dict-like object.
    """

    def __init__(
        self,
        filename: str,
        search_paths: list,
        defaults: dict = None,
        schema: dict = None,
    ):
        """Establishes a dict-like config object.

        Args:
            filename (str): file name without path
            search_paths (list): list of paths (strings) in priority order
            defaults (dict): a set of default objects (optional)
            schema (dict): a json schema definition for the config file (optional)

        Returns:
            None

        Raises:
            none

        """
        UserDict.__init__(self)
        self.defaults = defaults
        self.schema = schema
        self.path = self.find(filename, search_paths)
        self.read()
        self.validate()

    def find(self, filename: str, search_paths: list) -> str:
        """Routine for finding the config file.

        Searches the preferred paths, in preferred order, to locate specified config file.

        Args:
            filename (str): file name without path
            search_paths (list): list of paths (strings) in priority order

        Returns:
            str: path

        Raises:
            none

        """
        logger.debug(
            "find: params filename=%s, search_paths=%s", filename, search_paths
        )

        # See which config file exists, return the 1st one found
        for path in search_paths:
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path):
                logger.info("find: config located at path=%s", file_path)
                return file_path
        logger.info(
            "find: config file not found. filename=%s, search_paths=%s",
            filename,
            search_paths,
        )
        return None

    def read(self):
        """Load config from YAML or JSON file and merge defaults

        Args:
            none

        Returns:
            none

        Raises:
            none

        """
        logger.debug("read: config path=%s", self.path)

        self.data = {}

        raw_config = None
        if self.path and os.path.isfile(self.path):
            logger.info("read: loading config from file: %s", self.path)
            with open(self.path, "rt", encoding="utf_8") as config_file:
                if self.path.endswith(".yaml") or self.path.endswith(".yml"):
                    raw_config = yaml.safe_load(config_file.read())
                else:
                    raw_config = json.load(config_file)
        else:
            logger.info("read: config file not found. path=%s", self.path)
        logger.debug("read: raw_config=%s", json.dumps(raw_config))

        merged_config = {}
        if self.defaults:
            logger.debug("read: merging config defaults")
            mergedeep.merge(merged_config, self.defaults, raw_config)
        else:
            merged_config = raw_config
        logger.debug("read: merged_config=%s", json.dumps(merged_config))

        if merged_config:
            self.update(merged_config)

    def validate(self):
        """Validate config using json schema.

        Args:
            none

        Returns:
            none

        Raises:
            none

        """
        logger.debug("validate: config path=%s", self.path)

        if self.schema:
            jsonschema.validate(self.data, self.schema)
