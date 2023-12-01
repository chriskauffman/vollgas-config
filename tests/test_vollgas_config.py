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
from vollgas_config import __version__


def test_version():  # pylint: disable=missing-docstring
    assert __version__ == "1.1.0"
