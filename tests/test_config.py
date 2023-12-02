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
import json
import os.path

import pytest
import yaml

from vollgas_config import config


TEST_YAML_CONFIG_FILE = "test_config.yaml"
TEST_JSON_CONFIG_FILE = "test_config.json"
TEST_CONFIG = {
    "name": "resources/test_config.yaml",
    "test_compare": 200,
    "test_template_override": {"test_value_override": 1},
}
TEST_BAD_CONFIG = """Lorem ipsum dolor sit amet, consectetur adipiscing elit,
sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""


# pylint: disable=missing-docstring,redefined-outer-name
@pytest.fixture(scope="session")
def temp_config_dir(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("vollgas_config")
    return temp_dir


# pylint: disable=missing-docstring,redefined-outer-name
@pytest.fixture(scope="session")
def bad_json_config_file(temp_config_dir):
    file = os.path.join(temp_config_dir, "bad.json")
    with open(file, "w", encoding="utf_8") as json_file:
        json_file.write(TEST_BAD_CONFIG)
    return file


# pylint: disable=missing-docstring,redefined-outer-name
@pytest.fixture(scope="session")
def bad_txt_config_file(temp_config_dir):
    file = os.path.join(temp_config_dir, "bad.txt")
    with open(file, "w", encoding="utf_8") as txt_file:
        txt_file.write(TEST_BAD_CONFIG)
    return file


# pylint: disable=missing-docstring,redefined-outer-name
@pytest.fixture(scope="session")
def bad_yaml_config_file(temp_config_dir):
    file = os.path.join(temp_config_dir, "bad.yaml")
    with open(file, "w", encoding="utf_8") as yaml_file:
        yaml_file.write(TEST_BAD_CONFIG)
    return file


# pylint: disable=missing-docstring,redefined-outer-name
@pytest.fixture(scope="session")
def json_config_file(temp_config_dir):
    file = os.path.join(temp_config_dir, TEST_JSON_CONFIG_FILE)
    with open(file, "w", encoding="utf_8") as json_file:
        json_file.write(json.dumps(TEST_CONFIG))
    return file


# pylint: disable=missing-docstring,redefined-outer-name
@pytest.fixture(scope="session")
def yaml_config_file(temp_config_dir):
    file = os.path.join(temp_config_dir, TEST_YAML_CONFIG_FILE)
    with open(file, "w", encoding="utf_8") as yaml_file:
        yaml.dump(TEST_CONFIG, yaml_file, default_flow_style=False)
    return file


# pylint: disable=missing-docstring,redefined-outer-name
def test_find_config(temp_config_dir):
    file_list = []
    search_paths = []
    for path in (
        ".test_config_tool/",
        "local/",
        "etc/",
    ):
        file = os.path.join(temp_config_dir, path)
        os.mkdir(file)
        search_paths.append(file)
        file = os.path.join(file, TEST_YAML_CONFIG_FILE)
        with open(file, "w", encoding="utf_8") as yaml_file:
            yaml.dump(TEST_CONFIG, yaml_file, default_flow_style=False)
        file_list.append(file)

    for item in file_list:
        test_config = config.Config(TEST_YAML_CONFIG_FILE, search_paths)
        assert test_config.path == item
        os.remove(item)


# pylint: disable=missing-docstring,redefined-outer-name
def test_json_load_config(temp_config_dir, json_config_file):
    test_config = config.Config(
        TEST_JSON_CONFIG_FILE,
        (temp_config_dir,),
    )

    assert test_config.path is not None
    assert test_config.path == json_config_file


# pylint: disable=missing-docstring,redefined-outer-name
def test_yaml_load_config(temp_config_dir, yaml_config_file):
    test_config = config.Config(
        TEST_YAML_CONFIG_FILE,
        (temp_config_dir,),
    )

    assert test_config.path is not None
    assert test_config.path == yaml_config_file


# pylint: disable=missing-docstring,redefined-outer-name
def test_compare_load_config(temp_config_dir, json_config_file, yaml_config_file):
    test_config_json = config.Config(
        TEST_JSON_CONFIG_FILE,
        (temp_config_dir,),
    )
    test_config_yaml = config.Config(
        TEST_YAML_CONFIG_FILE,
        (temp_config_dir,),
    )

    assert test_config_json.path == json_config_file
    assert test_config_yaml.path == yaml_config_file
    assert test_config_json["test_compare"] == test_config_yaml["test_compare"]


def test_missing_file(temp_config_dir):
    test_config = config.Config(
        "no_file_1.json",
        (temp_config_dir,),
    )
    assert test_config.path is None


def test_bad_updated_path(temp_config_dir):
    test_config = config.Config(
        TEST_JSON_CONFIG_FILE,
        (temp_config_dir,),
    )

    assert test_config.data

    test_config.path = os.path.join(temp_config_dir, "no_file_2.json")
    test_config.read()

    assert test_config.data == {}


# def test_bad_json(temp_config_dir, bad_json_config_file):
#     test_config = config.Config(
#         bad_json_config_file,
#         (temp_config_dir,),
#     )

#     assert test_config.data


# pylint: disable=missing-docstring,redefined-outer-name
def test_default(temp_config_dir):
    test_template = {"test_template_default": {"test_value": 10}}
    test_config = config.Config(
        TEST_YAML_CONFIG_FILE,
        (temp_config_dir,),
        defaults=test_template,
    )

    assert (
        test_config["test_template_default"]["test_value"]
        == test_template["test_template_default"]["test_value"]
    )


# pylint: disable=missing-docstring,redefined-outer-name
def test_default_override(temp_config_dir):
    test_template = {
        "test_template_override": {
            "test_value_override": 0,
            "test_value_no_override": 0,
        }
    }
    test_config = config.Config(
        TEST_YAML_CONFIG_FILE,
        (temp_config_dir,),
        defaults=test_template,
    )

    assert test_config["test_template_override"]["test_value_override"] == 1
    assert (
        test_config["test_template_override"]["test_value_no_override"]
        == test_template["test_template_override"]["test_value_no_override"]
    )


# pylint: disable=missing-docstring,redefined-outer-name
def test_schema(temp_config_dir):
    test_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "test_compare": {"type": "number"},
        },
        "required": ["name", "test_compare"],
    }
    test_config = config.Config(
        TEST_YAML_CONFIG_FILE,
        (temp_config_dir,),
        schema=test_schema,
    )

    assert test_config["test_compare"] == TEST_CONFIG["test_compare"]


# pylint: disable=missing-docstring,redefined-outer-name
# def test_schema_error(temp_config_dir):
#     test_schema = {
#         "type": "object",
#         "properties": {
#             "name": {"type": "string"},
#             "test_compare": {"type": "number"},
#             "test_check": {"type": "boolean"},
#         },
#         "required": ["name", "test_compare", "test_check"],
#     }
#     test_config = config.Config(
#         TEST_YAML_CONFIG_FILE,
#         (temp_config_dir,),
#         schema=test_schema,
#     )

#     assert not test_config.data
