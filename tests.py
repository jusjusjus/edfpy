

def test_notation():
    from edfdb.notation import Label

    labels_by_type = {
        'EEG': (('M1-REF', 'M1-REF'), ('EEG F1-F2', 'F1-F2'), ('EEG O1-M2', 'O1-M2'), ('EEG C3-A2',
            'C3-M2'), ('EEG C3/A2', 'C3-M2'), ('EEG1.2', 'EEG1.2')),
        'EOG': (('EOG ROC-REF', 'EOG_R-REF'),),
        'EMG': (('EMG1.2', 'EMG1.2'), ('EMG-REF', 'EMG-REF')),
        'ECG': (('EEG EKG-REF', 'ECG-REF'), ('EEG EKG2-REF', 'ECG2-REF')),
    }

    for typ, labels in labels_by_type.items():
        for original, truth in labels:
            label = Label(original)
            assert label.is_type(label.type)
            assert label.is_type(typ) and truth == label, \
                    "{} (origin), got {} of type {}".format(original, label, label.type)


def test_notation_label_difference():
    from edfdb.notation import Label
    # classical rereferencing
    l1, l2 = Label('C4-M2'), Label('C3-M2')
    diff = l1-l2
    assert diff.is_type(l1.type)
    assert diff == 'C4-C3'
    # rereference with REF-type channel
    l1, l2 = Label('C4-M2'), Label('M1-M2')
    diff = l1-l2
    assert diff.is_type(l1.type)
    assert diff == 'C4-M1'
    # empty reference channel
    l1, l2 = Label('C4'), Label('C3')
    diff = l1-l2
    assert diff.is_type(l1.type)
    assert diff == 'C4-C3'
    # empty reference channel
    l1, l2 = Label('C4'), Label('M1')
    diff = l1-l2
    assert diff.is_type(l1.type)
    assert diff == 'C4-M1'

if __name__ == "__main__":
    test_notation()
    test_notation_label_difference()
    print("All tests passed")
