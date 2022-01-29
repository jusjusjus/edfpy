from pytest import fixture


@fixture
def test_header_field_bytes():
    return b'0       brux2                                                                                                                                                           04.02.0222.07.231536                                                100     1       5   '  # noqa: E501
