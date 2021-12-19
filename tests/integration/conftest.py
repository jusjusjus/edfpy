from os.path import join, exists, dirname

import pytest

from edfpy.header import Header


@pytest.fixture
def header():
    filepath = join(dirname(__file__), '..', '..', 'examples', 'sample.edf')
    assert exists(filepath), f"File {filepath} not existent"
    return Header.read_file(filepath)
