import pytest


@pytest.mark.parametrize("field,expected", [
    ('version', '0'),
    ('patient_id', 'brux2'),
    ('recording_id', ''),
    ('startdate', '04.02.02'),
    ('starttime', '22.07.23'),
    ('num_header_bytes', 1536),
    ('reserved', ''),
    ('num_records', 100),
    ('record_duration', 1.0),
    ('num_channels', 5),
])
def test_header(field, expected, header):
    """Checks header's `field` to be `expected`."""
    value = header.__getattribute__(field)
    assert value == expected, f"expected `{field}` `{value}` [{expected}]"
