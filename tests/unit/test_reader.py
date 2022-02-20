from datetime import datetime
from edfpy.label import Label
from edfpy.header import Header
from edfpy.reader import Reader
from edfpy.channel import Channel


def test_duration():
    record_duration = 10
    num_records = 10
    expected = record_duration * num_records
    header = Header(**{
        'record_duration': record_duration,
        'num_records': num_records,
    })
    reader = Reader(header, [])
    assert reader.duration == expected


def test_startdatetime():
    expected = datetime(2002, 2, 4, 22, 7, 23)
    header = Header(**{
        'startdate': '04.02.02',
        'starttime': '22.07.23',
    })
    reader = Reader(header, [])
    assert reader.startdatetime == expected


def test_labels_with_derivations():
    expected = ['F4-T8', 'T4-T8', 'F4-T4', 'T4-F4']
    first = Channel(**{
        'physical_dimension': 'uV',
        'num_samples_per_record': 20,
        'label': expected[0],
    })
    second = Channel(**{
        'physical_dimension': 'uV',
        'num_samples_per_record': 20,
        'label': expected[1]
    })
    reader = Reader(None, [first, second])
    assert set(reader.labels) == set(expected)


def test_required_from_requested():
    expected = ['F4-T8', 'T4-T8']
    first = Channel(**{
        'physical_dimension': 'uV',
        'num_samples_per_record': 20,
        'label': expected[0],
    })
    second = Channel(**{
        'physical_dimension': 'uV',
        'num_samples_per_record': 20,
        'label': expected[1]
    })
    reader = Reader(None, [first, second])
    requested = [Label('F4-T4')]
    assert set(reader.required_from_requested(requested)) == set(expected)
