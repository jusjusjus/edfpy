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
@pytest.mark.parametrize('filename', ['sample.edf'])
def test_header(field, expected, header):
    """Checks header's `field` to be `expected`."""
    value = header.__getattribute__(field)
    assert value == expected, f"expected `{field}` `{value}` [{expected}]"


@pytest.mark.parametrize('filename', ['sample.edf', 'sample2.edf'])
def test_build_channel_differences(header):
    header.build_channel_differences()
    label_channels = set(header.channel_by_label.keys())
    sr_channels = set(header.sampling_rate_by_label.keys())
    assert label_channels == sr_channels


@pytest.mark.parametrize('filename', ['sample2.edf'])
@pytest.mark.parametrize('depth, expected_labels', [
    (0, {'C4-M1', 'C4-P4', 'P4-O2'}),
    (1, {'C4-M1', 'C4-P4', 'P4-O2', 'P4-M1', 'M1-P4'}),
    (2, {'C4-M1', 'C4-P4', 'P4-O2', 'P4-M1', 'M1-P4',
         'M1-C4', 'P4-C4', 'M1-O2', 'O2-M1'}),
])
def test_build_channel_differences_depth(header, depth, expected_labels):
    header.build_channel_differences(depth=depth)
    labels = set(header.channel_by_label.keys())
    assert labels == expected_labels
