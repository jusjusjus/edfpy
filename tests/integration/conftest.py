from os.path import join, exists, dirname

from pytest import fixture


@fixture
def sample_filepath(filename):
    filepath = join(dirname(__file__), '..', '..', 'examples', filename)
    assert exists(filepath), f"File {filepath} not existent"
    return filepath
