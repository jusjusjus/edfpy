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


@pytest.mark.parametrize('first, second, expected', [
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
def test_is_compatible(first, second, expected):
    assert first.is_compatible(second) == expected
    assert second.is_compatible(first) == expected


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


@pytest.mark.parametrize('first, second, expected', [
    (Label('F4-F8'), Label('F8-T4'), Label('F4-T4')),
    (Label('F8'), Label('-T4'), Label('F8-T4')),
    (Label('-F8'), Label('T4'), Label('T4-F8')),
])
def test_add(first, second, expected):
    assert first + second == expected


@pytest.mark.parametrize('first, second', [
    (Label('F4-F8'), Label('T8-T4')),
    (Label('F4-F8'), Label('F4-T4')),
    (Label('F4'), Label('F8')),
    (Label('-F4'), Label('-F8')),
])
def test_add_raises(first, second):
    with pytest.raises(ValueError):
        assert first + second


@pytest.mark.parametrize('first, second, expected', [
    (Label('F4-F8'), Label('T4-F8'), Label('F4-T4')),
    (Label('F8-T4'), Label('F8-F4'), Label('F4-T4')),
    (Label('F8'), Label('F4'), Label('F8-F4')),
    (Label('-F8'), Label('-F4'), Label('F4-F8')),
])
def test_sub(first, second, expected):
    assert first - second == expected


@pytest.mark.parametrize('first, second', [
    (Label('F4-F8'), Label('T8-T4')),
    (Label('F4-F8'), Label('T4-F4')),
    (Label('-F4'), Label('F8')),
    (Label('F4'), Label('-F8')),
])
def test_sub_raises(first, second):
    with pytest.raises(ValueError):
        assert first - second


@pytest.mark.parametrize('first, second, expected', [
    (Label('F4-F8'), Label('T4-F8'), (Label('F4-T4'), '-')),
    (Label('F8'), Label('F4'), (Label('F8-F4'), '-')),
    (Label('F8-F4'), Label('T4-F8'), (Label('T4-F4'), '+')),
    (Label('-F8'), Label('F4'), (Label('F4-F8'), '+')),
])
def test_derive(first, second, expected):
    assert first.derive(second) == expected


@pytest.mark.parametrize('first, second', [
    (Label('F4-F8'), Label('T4-T3')),
    (Label('T4-F4'), Label('F8')),
])
def test_derive_raises(first, second):
    with pytest.raises(ValueError):
        first.derive(second)
