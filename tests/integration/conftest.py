from os.path import join, exists, dirname

import pytest

from edfpy.header import Header


@pytest.fixture
def header(filename):
    filepath = join(dirname(__file__), '..', '..', 'examples', filename)
    assert exists(filepath), f"File {filepath} not existent"
    return Header.read_file(filepath)
