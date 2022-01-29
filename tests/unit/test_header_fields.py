from io import BytesIO
from edfpy.header_fields import HeaderFields


def test_read(test_header_field_bytes):
    """test read header-field bytes from file"""
    expected = {
        'version': '0',
        'patient_id': 'brux2',
        'recording_id': '',
        'startdate': '04.02.02',
        'starttime': '22.07.23',
        'num_header_bytes': 1536,
        'reserved': '',
        'num_records': 100,
        'record_duration': 1.0,
        'num_channels': 5,
    }
    file = BytesIO(test_header_field_bytes)
    fields = HeaderFields.read(file)
    for key in expected:
        assert getattr(fields, key) == expected[key], key


def test_write(test_header_field_bytes):
    expected = {
        'version': '0',
        'patient_id': 'brux2',
        'recording_id': '',
        'startdate': '04.02.02',
        'starttime': '22.07.23',
        'num_header_bytes': 1536,
        'reserved': '',
        'num_records': 100,
        'record_duration': 1,
        'num_channels': 5,
    }
    fields = HeaderFields(**expected)
    file = BytesIO()
    fields.write(file)
    file.seek(0)
    content = file.read(256)
    assert content == test_header_field_bytes


def test_roundtrip():
    expected = {
        'version': '13',
        'patient_id': 'some-id',
        'recording_id': 'another-id',
        'startdate': '18.02.84',
        'starttime': '11:11:00',
        'num_header_bytes': 1000,
        'reserved': 'abracadabra',
        'num_records': 100,
        'record_duration': 2,
        'num_channels': 3,
    }
    fields = HeaderFields(**expected)
    file = BytesIO()
    fields.write(file)
    file.seek(0)
    fields = HeaderFields.read(file)
    for key in expected:
        assert getattr(fields, key) == expected[key], key
