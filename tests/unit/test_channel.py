from io import BytesIO
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
