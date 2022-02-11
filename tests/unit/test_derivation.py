import pytest
from edfpy.label import Label
from edfpy.channel import Channel

common_props = {
    'channel_type': 'EEG',
    'physical_dimension': 'uV',
    'num_samples_per_record': 256,
}


@pytest.fixture
def derivation(left_label, right_label):
    left = Channel(label=left_label, **common_props)
    right = Channel(label=right_label, **common_props)
    return left.derive(right)


@pytest.mark.parametrize('left_label, right_label', ['F7', 'M1'])
def test_common_props(derivation):
    for k, v in common_props.items():
        assert getattr(derivation, k) == v


@pytest.mark.parametrize('left_label, right_label', ['F7', 'M1'])
def test_label(derivation, left_label, right_label):
    label = Label(f"{left_label}-{right_label}")
    assert derivation.label == label
