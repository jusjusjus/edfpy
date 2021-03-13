from os.path import join, exists, dirname

import pytest

from edfdb.header import Header


@pytest.fixture
def header():
    filepath = join(dirname(__file__), '..', 'examples', 'sample.edf')
    assert exists(filepath), f"File {filepath} not existent"
    return Header.read_file(filepath)

@pytest.mark.parametrize("field,expected", [
    ('version',         '0'),
    ('patient_id',      'brux2'),
    ('recording_id',    ''),
    ('startdate',       '04.02.02'),
    ('starttime',       '22.07.23'),
    ('num_header_bytes', 1536),
    ('reserved',        ''),
    ('num_records',     100),
    ('record_duration', 1.0),
    ('num_channels',    5),
])
def test_header(field, expected, header):
    """Checks header's `field` to be `expected`."""
    assert header.__getattribute__(field) == expected, "expected `%s` `%s` [%s]"%(field, val, expected)
