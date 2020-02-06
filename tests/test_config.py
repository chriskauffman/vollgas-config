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
TEST_YAML_CONFIG_FILE = "test_config.yaml"
TEST_JSON_CONFIG_FILE = "test_config.json"
TEST_HOME_DIR = ".test_config_tool"
FILE_LIST = (
    "{0}/{1}".format(os.getcwd(), TEST_YAML_CONFIG_FILE),
    "{0}/{1}".format(HOME_CONFIG_DIR, TEST_YAML_CONFIG_FILE),
    "/usr/local/etc/{0}".format(TEST_YAML_CONFIG_FILE),
    "/etc/{0}".format(TEST_YAML_CONFIG_FILE),
)


def test_find_config():  # pylint: disable=missing-docstring
    os.mkdir(HOME_CONFIG_DIR)
    for file in FILE_LIST:
        with open(file, "w") as yaml_file:
            yaml.dump({"name": file}, yaml_file, default_flow_style=False)

    for item in FILE_LIST:
        test_config = config.Config(TEST_YAML_CONFIG_FILE, TEST_HOME_DIR)
        assert test_config.abs_filename == item
        os.remove(item)

    os.rmdir(HOME_CONFIG_DIR)


def test_json_load_config():  # pylint: disable=missing-docstring
    test_config = config.Config(
        resource_filename(__name__, "resources/{0}".format(TEST_JSON_CONFIG_FILE)),
        TEST_HOME_DIR,
    )
    assert test_config.abs_filename is not None
    assert test_config.abs_filename == resource_filename(
        __name__, "resources/{0}".format(TEST_JSON_CONFIG_FILE)
    )


def test_yaml_load_config():  # pylint: disable=missing-docstring
    test_config = config.Config(
        resource_filename(__name__, "resources/{0}".format(TEST_YAML_CONFIG_FILE)),
        TEST_HOME_DIR,
    )
    assert test_config.abs_filename is not None
    assert test_config.abs_filename == resource_filename(
        __name__, "resources/{0}".format(TEST_YAML_CONFIG_FILE)
    )


def test_compare_load_config():  # pylint: disable=missing-docstring
    test_config_json = config.Config(
        resource_filename(__name__, "resources/{0}".format(TEST_JSON_CONFIG_FILE)),
        TEST_HOME_DIR,
    )
    test_config_yaml = config.Config(
        resource_filename(__name__, "resources/{0}".format(TEST_YAML_CONFIG_FILE)),
        TEST_HOME_DIR,
    )
    assert test_config_json.data["test_compare"] == test_config_yaml.data["test_compare"]


def test_template_default():  # pylint: disable=missing-docstring
    test_template = {"test_template_default": {"test_value": 10}}
    test_config = config.Config(
        resource_filename(__name__, "resources/{0}".format(TEST_YAML_CONFIG_FILE)),
        TEST_HOME_DIR,
        template=test_template,
    )
    assert (
        test_config.data["test_template_default"]["test_value"]
        == test_template["test_template_default"]["test_value"]
    )


def test_template_override():  # pylint: disable=missing-docstring
    test_template = {
        "test_template_override": {
            "test_value_override": 0,
            "test_value_no_override": 0,
        }
    }
    test_config = config.Config(
        resource_filename(__name__, "resources/{0}".format(TEST_YAML_CONFIG_FILE)),
        TEST_HOME_DIR,
        template=test_template,
    )
    assert test_config.data["test_template_override"]["test_value_override"] == 1
    assert (
        test_config.data["test_template_override"]["test_value_no_override"]
        == test_template["test_template_override"]["test_value_no_override"]
    )
