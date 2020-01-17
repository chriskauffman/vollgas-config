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
import yaml

from pkg_resources import resource_filename


class Config:
    """Config Class

    Finds and loads config object
    """

    def __init__(
        self, config_filename: str, home_config_dir: str, logger: logging.Logger = None
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
        self.config_fq_filename = self.find_config(config_filename)
        self.data = self.load_yaml_config(self.config_fq_filename)

    def find_config(self, config_filename: str, logger: logging.Logger = None) -> str:
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
            "{0}/{1}".format(os.getcwd(), config_filename),
            "{0}/{1}/{2}".format(
                os.path.expanduser("~"), self._home_config_dir, config_filename
            ),
            "/usr/local/etc/{0}".format(config_filename),
            "/etc/{0}".format(config_filename),
            resource_filename(__name__, "resources/{0}".format(config_filename)),
        )

        # See which config file exists, return the 1st one found
        for config_file in config_file_list:
            if os.path.exists(config_file):
                logger.debug("find_config: using %s", config_file)
                return config_file

        return None

    # ToDo: Add JSON load
    # def load_json_config (config_fq_filename: str, logger: logging.Logger = None) -> dict:

    def load_yaml_config(
        self, config_fq_filename: str, logger: logging.Logger = None
    ) -> dict:
        """Routine for loading config from YAML file.

        Args:
            config_fq_filename (str): fully-qualified file name

        Returns:
            dict: config dictionary

        Raises:
            none

        """
        logger = logger or logging.getLogger(__name__)

        logger.debug("load_config params: config_fq_filename=%s", config_fq_filename)

        config = {}
        if config_fq_filename and os.path.exists(config_fq_filename):
            logger.info("Reading config from file: %s", config_fq_filename)
            try:
                with open(config_fq_filename, "rt") as config_file:
                    config = yaml.safe_load(config_file.read())
            except IOError:
                logger.error("Config file IOError: %s", config_fq_filename)
            # Adding reference to filename used when retrieving config
            if config is None:
                config = {}
            config["_ConfigFQFilename"] = config_fq_filename
            logger.debug(json.dumps(config))
        else:
            logger.error("Config file %s not found.", config_fq_filename)
            return None
        return config
