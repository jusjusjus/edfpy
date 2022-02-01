from datetime import datetime

import numpy as np
import pytest

from edfpy.reader import Reader


@pytest.mark.parametrize('filename, duration', [
    ('sample.edf', 100.0),
    ('sample2.edf', 10.0),
])
def test_duration(sample_filepath, duration):
    """test Reader.duration"""
    reader = Reader(sample_filepath)
    assert reader.duration == duration


@pytest.mark.parametrize('filename, startdatetime', [
    ('sample.edf', datetime(2002, 2, 4, 22, 7, 23)),
    ('sample2.edf', datetime(2007, 7, 9, 22, 40, 41)),
])
def test_startdatetime(sample_filepath, startdatetime):
    """test Reader.startdatetime"""
    reader = Reader(sample_filepath)
    assert reader.startdatetime == startdatetime


@pytest.mark.parametrize('filename', ['sample.edf'])
def test_get_physical_samples_subset(sample_filepath):
    """test Reader.startdatetime"""
    expected = ['Fp2-F4']
    reader = Reader(sample_filepath)
    signals = reader.get_physical_samples(labels=expected)
    assert set(signals.keys()) == set(expected)
    other = reader.get_physical_samples()
    assert np.all(signals[expected[0]] == other[expected[0]])


@pytest.mark.parametrize('filename', ['sample.edf'])
def test_get_physical_samples(sample_filepath, sample_data):
    """test Reader.startdatetime"""
    reader = Reader(sample_filepath)
    signals = reader.get_physical_samples()
    assert set(signals.keys()) == set(sample_data.columns)
    for label, expected in sample_data.items():
        signal = signals[label]
        assert signal.shape == expected.shape, label
        assert signal == pytest.approx(expected, rel=1e-4), label


@pytest.mark.parametrize('filename', ['sample.edf'])
def test_get_physical_samples_in_range(sample_filepath, sample_data):
    """test Reader.startdatetime"""
    t0, dt = 1.0, 0.503  # seconds
    reader = Reader(sample_filepath)
    signals = reader.get_physical_samples(t0, dt)
    assert set(signals.keys()) == set(sample_data.columns)
    for label, data in sample_data.items():
        expected = data.loc[t0:t0 + dt]
        signal = signals[label]
        assert signal.shape == expected.shape, label
        assert signal == pytest.approx(expected, rel=1e-4), label
