from io import BytesIO
from edfpy.channel_fields import ChannelFields


def test_read(test_channel_field_bytes, test_channel_field_content):
    """test read channel-field bytes from file"""
    expected = test_channel_field_content
    file = BytesIO(test_channel_field_bytes)
    channels = ChannelFields.read(file, len(expected))
    for exp, channel in zip(expected, channels):
        for key in exp:
            print(exp[key], getattr(channel, key), 'x')
            assert getattr(channel, key) == exp[key], key


def test_write(test_channel_field_bytes, test_channel_field_content):
    """test write channel-fields to file"""
    contents = test_channel_field_content
    channels = [ChannelFields(spec, **content)
                for spec, content in enumerate(contents)]
    file = BytesIO()
    ChannelFields.write(file, channels)
    file.seek(0)
    expected = file.read()
    assert expected == test_channel_field_bytes
