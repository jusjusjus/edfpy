from typing import Union
from collections import namedtuple

Field = namedtuple('Field', 'name, type, size')


def normalize(dtype, value: Union[str, bytes]):
    if isinstance(value, str):
        value = value.strip('\x00').strip(' ')
    elif isinstance(value, bytes):
        value = value.strip(b'\x00')
    else:
        AttributeError(f"Unknown type {type(value)}")

    if dtype is str:
        if isinstance(value, bytes):
            try:
                return str(value, 'ascii')
            except BaseException:
                return str(value, 'latin1')
        else:
            return value

    else:
        return dtype(value)


def serialize(value, size):
    format_str = '{:<%i}' % size if size else '{}'
    return bytes(format_str.format(value), 'latin1')
