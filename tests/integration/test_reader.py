from os.path import splitext
from datetime import datetime

import numpy as np
import pandas as pd
import pytest

from edfpy.reader import Reader
from edfpy.channel import Annotation


@pytest.mark.parametrize('filename, duration', [
    ('sample.edf', 100.0),
    ('sample2.edf', 10.0),
    ('edfp-sample.edf', 25.6),
])
def test_duration(sample_filepath, duration):
    """test Reader.duration"""
    reader = Reader.open(sample_filepath)
    assert reader.duration == duration


@pytest.mark.parametrize('filename, startdatetime', [
    ('sample.edf', datetime(2002, 2, 4, 22, 7, 23)),
    ('sample2.edf', datetime(2007, 7, 9, 22, 40, 41)),
    ('edfp-sample.edf', datetime(2018, 8, 27, 11, 25, 11)),
])
def test_startdatetime(sample_filepath, startdatetime):
    """test Reader.startdatetime"""
    reader = Reader.open(sample_filepath)
    assert reader.startdatetime == startdatetime


@pytest.mark.parametrize('filename, channel', [
    ('sample.edf', 'Fp2-F4'),
    ('sample2.edf', 'C4-M1'),
])
def test_get_physical_samples_subset(sample_filepath, channel):
    """test Reader.startdatetime"""
    expected = [channel]
    reader = Reader.open(sample_filepath)
    signals = reader.get_physical_samples(labels=expected)
    assert set(signals.keys()) == set(expected)
    other = reader.get_physical_samples()
    assert np.all(signals[expected[0]] == other[expected[0]])


@pytest.mark.parametrize('filename', ['sample.edf', 'sample2.edf'])
def test_get_physical_samples(sample_filepath, sample_data):
    """test Reader.startdatetime"""
    reader = Reader.open(sample_filepath)
    signals = reader.get_physical_samples()
    assert set(signals.keys()) == set(sample_data.columns)
    for label, expected in sample_data.items():
        signal = signals[label]
        assert signal.shape == expected.shape, label
        assert signal == pytest.approx(expected, rel=1e-4), label


@pytest.mark.parametrize('filename', ['sample.edf', 'sample2.edf'])
def test_get_physical_samples_in_range(sample_filepath, sample_data):
    """test Reader.startdatetime"""
    t0, dt = 1.0, 0.503  # seconds
    reader = Reader.open(sample_filepath)
    signals = reader.get_physical_samples(t0, dt)
    assert set(signals.keys()) == set(sample_data.columns)
    for label, data in sample_data.items():
        expected = data.loc[t0:t0 + dt]
        signal = signals[label]
        assert signal.shape == expected.shape, label
        assert signal == pytest.approx(expected, rel=1e-4), label


@pytest.mark.parametrize('filename', ['edfp-sample.edf'])
def test_edfp_annotations_channel(filename, sample_filepath):
    """test AnnotationChannel.annotations"""
    annots_filepath = splitext(sample_filepath)[0] + '_annotations.csv'
    expected_df = pd.read_csv(annots_filepath, index_col=False)
    expected = [Annotation(*annot) for _, annot in expected_df.iterrows()]
    reader = Reader.open(sample_filepath)
    annots_channel = reader.channel_by_label['ANNOTATIONS']
    annotations = annots_channel.annotations
    assert annotations == expected
