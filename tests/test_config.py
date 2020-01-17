#!/usr/bin/env python
"""Test routines for configtool. For use with pytest.

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
from pkg_resources import resource_filename

import os.path
import yaml

# from pkg_resources import resource_filename

from vollgas_config import config


HOME_CONFIG_DIR = "{0}/.test_config_tool".format(os.path.expanduser("~"))
TEST_CONFIG_FILE = "test_config.yaml"
FILE_LIST = (
    "{0}/{1}".format(os.getcwd(), TEST_CONFIG_FILE),
    "{0}/{1}".format(HOME_CONFIG_DIR, TEST_CONFIG_FILE),
    "/usr/local/etc/{0}".format(TEST_CONFIG_FILE),
    # "/etc/{0}".format(TEST_CONFIG_FILE),
    # resource_filename(__name__, "resources/{0}".format(TEST_CONFIG_FILE)),
)


def setup_module():
    os.mkdir(HOME_CONFIG_DIR)

    for file in FILE_LIST:
        with open(file, "w") as yaml_file:
            yaml.dump({"name": file}, yaml_file, default_flow_style=False)


# def test_find_config():  # pylint: disable=missing-docstring
#    assert configtool.find_config(TEST_CONFIG_FILE) == "{0}/{1}".format(os.getcwd(), TEST_CONFIG_FILE)


def test_find_config():  # pylint: disable=missing-docstring
    test_config = config.Config(TEST_CONFIG_FILE, ".test_config_tool")
    for item in FILE_LIST:
        assert test_config.find_config(TEST_CONFIG_FILE) == item
        os.remove(item)


def test_load_config():  # pylint: disable=missing-docstring
    test_config = config.Config(TEST_CONFIG_FILE, ".test_config_tool")
    assert (
        test_config.load_yaml_config(
            resource_filename(__name__, "resources/{0}".format(TEST_CONFIG_FILE))
        )
        is not None
    )


def test_load_config_with_template():  # pylint: disable=missing-docstring
    test_config = config.Config(
        TEST_CONFIG_FILE, ".test_config_tool", template={"test_template": 10}
    )
    assert test_config.data["test_template"] == 10


def teardown_module():
    os.rmdir(HOME_CONFIG_DIR)
