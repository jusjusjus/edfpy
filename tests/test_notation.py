import pytest

from edfdb.notation import Label


@pytest.mark.parametrize("original,normalized,typ", [
    ('M1-REF',      'M1-REF',   'EEG'),
    ('EEG F1-F2',   'F1-F2',    'EEG'),
    ('EEG O1-M2',   'O1-M2',    'EEG'),
    ('EEG C3/A2',   'C3-M2',    'EEG'),
    ('EEG1.2',      'EEG1.2',   'EEG'),
    ('EOG ROC-REF', 'EOG_R-REF','EOG'),
    ('EMG1.2',      'EMG1.2',   'EMG'),
    ('EMG-REF',     'EMG-REF',  'EMG'),
    ('EEG EKG-REF', 'ECG-REF',  'ECG'),
    ('EEG EKG2-REF','ECG2-REF', 'ECG'),
])
def test_normalization(original, normalized, typ):
    """Tests that `edfdb.Label` transforms `original` to `normalized` and infers `typ` as type."""
    label = Label(original)
    assert label.is_type(label.type)
    assert label.is_type(typ) and normalized == label, \
            "{} (origin), got {} of type {}".format(original, label, label.type)


@pytest.mark.parametrize("left,right,difference", [
    ('C4-M2', 'C3-M2', 'C4-C3'),
    ('C4', 'C3', 'C4-C3'),
    ('C4-M2', 'M1-M2', 'C4-M1'),
    ('C4', 'M1', 'C4-M1'),
])
def test_label_difference(left, right, difference):
    """Tests that differences of labels are computed and cast correctly."""
    l1, l2 = Label(left), Label(right)
    diff = l1-l2
    assert diff.is_type(l1.type)
    assert diff == difference 
