from io import BytesIO

import pytest

from edfpy.channel import Channel


def test_read(channel_bytes, channel_content):
    """test read channel-field bytes from file"""
    expected = channel_content
    file = BytesIO(channel_bytes)
    channels = Channel.read(file, len(expected))
    for exp, channel in zip(expected, channels):
        for key in exp:
            print(exp[key], getattr(channel, key), 'x')
            assert getattr(channel, key) == exp[key], key


def test_write(channel_bytes, channel_content):
    """test write channel-fields to file"""
    contents = channel_content
    channels = [Channel(spec, **content)
                for spec, content in enumerate(contents)]
    file = BytesIO()
    Channel.write(file, channels)
    file.seek(0)
    expected = file.read()
    assert expected == channel_bytes


@pytest.mark.parametrize('label, expected', [
    ('F4-F8', False),
    ('F4-T4', True),
])
def test_is_compatible_label(label, expected):
    first = Channel(**{
        'physical_dimension': 'mV',
        'num_samples_per_record': 20,
        'label': label,
    })
    second = Channel(**{
        'physical_dimension': 'mV',
        'num_samples_per_record': 20,
        'label': 'T4-T8',
    })
    assert first.is_compatible(second) == expected


@pytest.mark.parametrize('num_samples, expected', [
    (25, False),
    (20, True),
])
def test_is_compatible_num_samples(num_samples, expected):
    first = Channel(**{
        'physical_dimension': 'mV',
        'num_samples_per_record': num_samples,
        'label': 'F4-T8',
    })
    second = Channel(**{
        'physical_dimension': 'mV',
        'num_samples_per_record': 20,
        'label': 'T4-T8',
    })
    assert first.is_compatible(second) == expected


@pytest.mark.parametrize('units, expected', [
    ('uV', False),
    ('mV', True),
])
def test_is_compatible_units(units, expected):
    first = Channel(**{
        'physical_dimension': units,
        'num_samples_per_record': 20,
        'label': 'F4-T8',
    })
    second = Channel(**{
        'physical_dimension': 'mV',
        'num_samples_per_record': 20,
        'label': 'T4-T8',
    })
    assert first.is_compatible(second) == expected
