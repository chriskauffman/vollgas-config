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

import jsonschema
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
        new_dir = os.path.join(temp_config_dir, path)
        os.makedirs(new_dir)
        search_paths.append(new_dir)
        new_file = os.path.join(new_dir, TEST_YAML_CONFIG_FILE)
        with open(new_file, "w", encoding="utf_8") as yaml_file:
            yaml.dump(TEST_CONFIG, yaml_file, default_flow_style=False)
        file_list.append(new_file)

    for item in file_list:
        test_config = config.Config(TEST_YAML_CONFIG_FILE, search_paths)
        assert test_config.path == item
        os.remove(item)


# pylint: disable=missing-docstring,redefined-outer-name
def test_json_load_config(json_config_file):
    test_config = config.Config(
        os.path.basename(json_config_file),
        (os.path.dirname(json_config_file),),
    )

    assert test_config.path is not None
    assert test_config.path == json_config_file


# pylint: disable=missing-docstring,redefined-outer-name
def test_yaml_load_config(yaml_config_file):
    test_config = config.Config(
        os.path.basename(yaml_config_file),
        (os.path.dirname(yaml_config_file),),
    )

    assert test_config.path is not None
    assert test_config.path == yaml_config_file


# pylint: disable=missing-docstring,redefined-outer-name
def test_compare_load_config(json_config_file, yaml_config_file):
    test_config_json = config.Config(
        os.path.basename(json_config_file),
        (os.path.dirname(json_config_file),),
    )
    test_config_yaml = config.Config(
        os.path.basename(yaml_config_file),
        (os.path.dirname(yaml_config_file),),
    )

    assert test_config_json.path == json_config_file
    assert test_config_yaml.path == yaml_config_file
    assert test_config_json["test_compare"] == test_config_yaml["test_compare"]


def test_missing_file(temp_config_dir):
    """Test for missing config file"""
    test_config = config.Config(
        "no_file_1.json",
        (temp_config_dir,),
    )
    assert test_config.path is None
    assert test_config.data == {}


def test_bad_updated_path(temp_config_dir, json_config_file):
    """Test for path when updated after instantiation"""
    test_config = config.Config(
        os.path.basename(json_config_file),
        (os.path.dirname(json_config_file),),
    )

    assert test_config.data is not None
    assert test_config.data != {}

    test_config.path = os.path.join(temp_config_dir, "no_file_2.json")
    test_config.read()

    assert test_config.data == {}


def test_bad_json(bad_json_config_file):
    """Test for correct error if JSON load fails"""
    with pytest.raises(json.decoder.JSONDecodeError):
        config.Config(
            os.path.basename(bad_json_config_file),
            (os.path.dirname(bad_json_config_file),),
        )


def test_bad_txt(bad_txt_config_file):
    """Test for correct error if JSON load fails.

    If file is not identified as yaml, all files should attempt json load.
    """
    with pytest.raises(json.decoder.JSONDecodeError):
        config.Config(
            os.path.basename(bad_txt_config_file),
            (os.path.dirname(bad_txt_config_file),),
        )


def test_bad_yaml(bad_yaml_config_file):
    """Test for correct error when yaml load fails"""
    with pytest.raises(ValueError):
        config.Config(
            os.path.basename(bad_yaml_config_file),
            (os.path.dirname(bad_yaml_config_file),),
        )


# pylint: disable=redefined-outer-name
def test_default(yaml_config_file):
    """Tests that defaults are loaded into the config"""
    test_template = {"test_template_default": {"test_value": 10}}
    test_config = config.Config(
        os.path.basename(yaml_config_file),
        (os.path.dirname(yaml_config_file),),
        defaults=test_template,
    )

    assert (
        test_config["test_template_default"]["test_value"]
        == test_template["test_template_default"]["test_value"]
    )


def test_default_missing_file(temp_config_dir):
    """Test for missing config file"""
    test_template = {
        "test_template_override": {
            "test_value_override": 0,
            "test_value_no_override": 0,
        }
    }
    test_config = config.Config(
        "no_file_1.json",
        (temp_config_dir,),
        defaults=test_template,
    )
    assert test_config.path is None
    assert (
        test_config["test_template_override"]["test_value_no_override"]
        == test_template["test_template_override"]["test_value_no_override"]
    )


# pylint: disable=redefined-outer-name
def test_default_override(yaml_config_file):
    """Tests that config values override defaults"""
    test_template = {
        "test_template_override": {
            "test_value_override": 0,
            "test_value_no_override": 0,
        }
    }
    test_config = config.Config(
        os.path.basename(yaml_config_file),
        (os.path.dirname(yaml_config_file),),
        defaults=test_template,
    )

    assert test_config["test_template_override"]["test_value_override"] == 1
    assert (
        test_config["test_template_override"]["test_value_no_override"]
        == test_template["test_template_override"]["test_value_no_override"]
    )


# pylint: disable=redefined-outer-name
def test_good_schema(yaml_config_file):
    """Test a correct schema"""
    test_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "test_compare": {"type": "number"},
        },
        "required": ["name", "test_compare"],
    }
    test_config = config.Config(
        os.path.basename(yaml_config_file),
        (os.path.dirname(yaml_config_file),),
        schema=test_schema,
    )

    assert test_config["test_compare"] == TEST_CONFIG["test_compare"]


# pylint: disable=redefined-outer-name
def test_empty_schema(yaml_config_file):
    """Test empty schema

    Tests that None or an empty schema dict has no impact on config.
    """
    test_config = config.Config(
        os.path.basename(yaml_config_file),
        (os.path.dirname(yaml_config_file),),
        schema={},
    )

    assert test_config["test_compare"] == TEST_CONFIG["test_compare"]

    test_config.schema = {}
    test_config.validate()
    assert test_config["test_compare"] == TEST_CONFIG["test_compare"]

    test_config = config.Config(
        os.path.basename(yaml_config_file),
        (os.path.dirname(yaml_config_file),),
        schema=None,
    )

    assert test_config["test_compare"] == TEST_CONFIG["test_compare"]

    test_config.schema = None
    test_config.validate()
    assert test_config["test_compare"] == TEST_CONFIG["test_compare"]


# pylint: disable=redefined-outer-name
def test_bad_schema(yaml_config_file):
    """Test schema failure

    Test should succeed if the schema is invalid.
    """
    with pytest.raises(jsonschema.exceptions.SchemaError):
        config.Config(
            os.path.basename(yaml_config_file),
            (os.path.dirname(yaml_config_file),),
            schema={"type": "bad type"},
        )


# pylint: disable=redefined-outer-name
def test_validation_error(yaml_config_file):
    """Test schema validation failure

    Test should succeed if the validation fails.
    test_check is not in the config.
    """
    test_config_var = "test_check"
    assert not TEST_CONFIG.get(test_config_var)

    test_schema = {
        "type": "object",
        "properties": {
            test_config_var: {"type": "boolean"},
        },
        "required": [test_config_var],
    }
    with pytest.raises(jsonschema.exceptions.ValidationError):
        config.Config(
            os.path.basename(yaml_config_file),
            (os.path.dirname(yaml_config_file),),
            schema=test_schema,
        )
