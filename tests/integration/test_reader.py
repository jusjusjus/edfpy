from datetime import datetime

import pytest

from edfpy.reader import Reader


@pytest.mark.parametrize('filename, duration', [
    ('sample.edf', 100.0),
    ('sample2.edf', 10.0),
])
def test_duration(sample_filepath, duration):
    """test Reader.duration"""
    reader = Reader(sample_filepath)
    assert reader.duration == duration


@pytest.mark.parametrize('filename, startdatetime', [
    ('sample.edf', datetime(2002, 2, 4, 22, 7, 23)),
    ('sample2.edf', datetime(2007, 7, 9, 22, 40, 41)),
])
def test_startdatetime(sample_filepath, startdatetime):
    """test Reader.startdatetime"""
    reader = Reader(sample_filepath)
    assert reader.startdatetime == startdatetime
