from os.path import join, exists, dirname, splitext

import pandas as pd

from pytest import fixture


@fixture
def sample_filepath(filename):
    filepath = join(dirname(__file__), '..', '..', 'edfs', filename)
    assert exists(filepath), f"File {filepath} not existent"
    return filepath


@fixture
def sample_data(sample_filepath):
    filepath = splitext(sample_filepath)[0] + '.csv'
    df = pd.read_csv(filepath)
    return df.set_index('Time')
