import pytest

from edfpy.reader import Reader


@pytest.mark.parametrize('filename, duration', [
    ('sample.edf', 100.0),
    ('sample2.edf', 10.0),
])
def test_duration(sample_filepath, duration):
    reader = Reader(sample_filepath)
    assert reader.duration == duration
