from io import BytesIO
from edfpy.channel_fields import ChannelFields


def test_read(channel_field_bytes, channel_field_content):
    """test read channel-field bytes from file"""
    expected = channel_field_content
    file = BytesIO(channel_field_bytes)
    channels = ChannelFields.read(file, len(expected))
    for exp, channel in zip(expected, channels):
        for key in exp:
            print(exp[key], getattr(channel, key), 'x')
            assert getattr(channel, key) == exp[key], key


def test_write(channel_field_bytes, channel_field_content):
    """test write channel-fields to file"""
    contents = channel_field_content
    channels = [ChannelFields(spec, **content)
                for spec, content in enumerate(contents)]
    file = BytesIO()
    ChannelFields.write(file, channels)
    file.seek(0)
    expected = file.read()
    assert expected == channel_field_bytes
