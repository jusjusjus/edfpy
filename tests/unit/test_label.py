import pytest

from edfpy.label import Label


@pytest.mark.parametrize('label, expected', [
    ('F4-F8', ['F4', 'F8']),
    ('F4', ['F4', None]),
    ('-F4', [None, 'F4']),
])
def test_parts_left_right(label, expected):
    lab = Label(label)
    assert lab.left == expected[0]
    assert lab.right == expected[1]
    assert lab.parts == expected


@pytest.mark.parametrize('label1, label2, expected', [
    (Label('F4-F8'), Label('T4-T8'), False),
    (Label('F4'), Label('T4-T8'), False),
    (Label('F4-T4'), Label('T4-T8'), True),
    (Label('T4-F4'), Label('T4-T8'), True),
    (Label('F4-T8'), Label('T4-T8'), True),
    (Label('T8-F4'), Label('T4-T8'), True),
    (Label('T4'), Label('T4-T8'), True),
    (Label('T8'), Label('T4-T8'), True),
    (Label('T8'), Label('T4'), True),
    (Label('-T8'), Label('T4'), True),
])
def test_has_common_parts(label1, label2, expected):
    assert label1.has_common_part(label2) == expected
    assert label2.has_common_part(label1) == expected


@pytest.mark.parametrize('label, expected', [
    (Label('F4-F8'), Label('F8-F4')),
    (Label('F4'), Label('-F4')),
])
def test_invert(label, expected):
    assert -label == expected


@pytest.mark.parametrize('label', [
    Label('F4-F8'), Label('F4'), Label('-F4'),
])
def test_double_invert(label):
    assert -(-label) == label


@pytest.mark.parametrize('label1, label2, expected', [
    (Label('F4-F8'), Label('F8-T4'), Label('F4-T4')),
    (Label('F8'), Label('-T4'), Label('F8-T4')),
    (Label('-F8'), Label('T4'), Label('T4-F8')),
])
def test_add(label1, label2, expected):
    assert label1 + label2 == expected


@pytest.mark.parametrize('label1, label2', [
    (Label('F4-F8'), Label('T8-T4')),
    (Label('F4-F8'), Label('F4-T4')),
    (Label('F4'), Label('F8')),
    (Label('-F4'), Label('-F8')),
])
def test_add_raises(label1, label2):
    with pytest.raises(ValueError):
        assert label1 + label2


@pytest.mark.parametrize('label1, label2, expected', [
    (Label('F4-F8'), Label('T4-F8'), Label('F4-T4')),
    (Label('F8-T4'), Label('F8-F4'), Label('F4-T4')),
    (Label('F8'), Label('F4'), Label('F8-F4')),
    (Label('-F8'), Label('-F4'), Label('F4-F8')),
])
def test_sub(label1, label2, expected):
    assert label1 - label2 == expected


@pytest.mark.parametrize('label1, label2', [
    (Label('F4-F8'), Label('T8-T4')),
    (Label('F4-F8'), Label('T4-F4')),
    (Label('-F4'), Label('F8')),
    (Label('F4'), Label('-F8')),
])
def test_sub_raises(label1, label2):
    with pytest.raises(ValueError):
        assert label1 - label2
