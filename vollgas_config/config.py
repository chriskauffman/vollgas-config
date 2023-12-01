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
import json
import logging
import os.path

import mergedeep
import yaml


# pylint: disable=too-few-public-methods
class Config:
    """Config Class

    Finds and loads config object
    """

    def __init__(
        self,
        config_filename: str,
        home_config_dir: str,
        template: dict = None,
    ):
        """Routine for finding the config file.

        Searches the preferred paths, in preferred order, to locate specified config file.

        Args:
            config_filename (str): file name without path
            home_config_dir (str): directory name for app config, example ".app"

        Returns:
            None

        Raises:
            none

        """
        self._home_config_dir = home_config_dir
        if os.path.isfile(config_filename):
            self.abs_filename = os.path.abspath(config_filename)
        else:
            self.abs_filename = self._find_config(config_filename)

        loaded_config = self._load_config(self.abs_filename)
        if template is not None and loaded_config is not None:
            # self.data = {**template, **loaded_config}
            self.data = {**template}
            mergedeep.merge(self.data, loaded_config)
        elif template is not None and loaded_config is None:
            self.data = {**template}
        elif template is None and loaded_config is not None:
            self.data = {**loaded_config}
        else:
            self.data = None

    def _find_config(self, config_filename: str, logger: logging.Logger = None) -> str:
        """Routine for finding the config file.

        Searches the preferred paths, in preferred order, to locate specified config file.

        Args:
            config_filename (str): file name without path

        Returns:
            str: fully-qualified file name

        Raises:
            none

        """
        logger = logger or logging.getLogger(__name__)

        logger.debug("find_config params: config_filename=%s", config_filename)

        # Build prioritized list of config files
        config_file_list = (
            os.path.abspath(config_filename),
            f'{os.path.expanduser("~")}/{self._home_config_dir}/{config_filename}',
            f"/usr/local/etc/{config_filename}",
            f"/etc/{config_filename}",
        )

        # See which config file exists, return the 1st one found
        for config_file in config_file_list:
            if os.path.isfile(config_file):
                logger.debug("find_config: using %s", config_file)
                return config_file

        return None

    def _load_config(
        self, config_abs_filename: str, logger: logging.Logger = None
    ) -> dict:
        """Routine for loading config from YAML or JSON file.

        Args:
            config_abs_filename (str): fully-qualified file name

        Returns:
            dict: config dictionary

        Raises:
            none

        """
        logger = logger or logging.getLogger(__name__)

        logger.debug("load_config params: config_abs_filename=%s", config_abs_filename)

        config = {}
        if config_abs_filename and os.path.isfile(config_abs_filename):
            logger.info("Reading config from file: %s", config_abs_filename)
            try:
                with open(config_abs_filename, "rt", encoding="utf_8") as config_file:
                    if config_abs_filename.endswith(
                        ".yaml"
                    ) or config_abs_filename.endswith(".yml"):
                        config = yaml.safe_load(config_file.read())
                    elif config_abs_filename.endswith(".json"):
                        config = json.load(config_file)
                    else:
                        logger.error("Bad file: %s", config_abs_filename)
            except IOError:
                logger.error("Config file IOError: %s", config_abs_filename)
            # Adding reference to filename used when retrieving config
            if config is None:
                config = {}
            config["_ConfigFQFilename"] = config_abs_filename
            logger.debug(json.dumps(config))
        else:
            logger.error("Config file %s not found.", config_abs_filename)
            return None
        return config
