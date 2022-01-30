import numpy as np

from edfpy.blob import read_blob, write_blob


def blob_from_arrays(arrs, record_lengths):
    arrs = [arr.reshape((-1, n)) for arr, n in zip(arrs, record_lengths)]
    arrs = np.concatenate(arrs, axis=1)
    return arrs.tobytes()


def test_read_blob(tmp_path):
    record_lengths = [8, 16, 4]
    expected_signals = [
        np.arange(4 * 128, 6 * 128).astype(np.int16),
        np.arange(4 * 128).astype(np.int16),
        np.arange(6 * 128, 7 * 128).astype(np.int16),
    ]
    # write expected_signals as blob to temporary file
    filepath = tmp_path / 'test_read_blob'
    with open(filepath, 'wb') as fp:
        blob = blob_from_arrays(expected_signals, record_lengths)
        fp.write(blob)

    signals = read_blob(filepath, 0, record_lengths)
    for signal, expected in zip(signals, expected_signals):
        assert np.all(signal == expected)


def test_write_blob(tmp_path):
    record_lengths = [8, 16, 4]
    expected_signals = [
        np.arange(4 * 128, 6 * 128).astype(np.int16),
        np.arange(4 * 128).astype(np.int16),
        np.arange(6 * 128, 7 * 128).astype(np.int16),
    ]
    filepath = tmp_path / 'test_write_blob'
    with open(filepath, 'wb') as fp:
        write_blob(fp, expected_signals, record_lengths)

    signals = read_blob(filepath, 0, record_lengths)
    for signal, expected in zip(signals, expected_signals):
        assert np.all(signal == expected)
