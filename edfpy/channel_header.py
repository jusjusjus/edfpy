from typing import List, Union

import numpy as np

from .notation import Label, convert_units
from .channel_difference import ChannelDifference
from .field import Field

default_dtype = np.float32


class ChannelHeader:
    _fields = [
        Field('label', str, 16),
        Field('channel_type', str, 80),
        Field('physical_dimension', str, 8),
        Field('physical_minimum', float, 8),
        Field('physical_maximum', float, 8),
        Field('digital_minimum', int, 8),
        Field('digital_maximum', int, 8),
        Field('prefiltering', str, 80),
        Field('num_samples_per_record', int, 8),
        Field('reserved', str, 32)
    ]

    # _num_channel_header_bytes = sum(f.size for f in _fields)
    _num_header_bytes = 256

    def __init__(self, specifier):
        """
        Arguments:
            specifier: specifies the channel construction,
            typically the reference index in a data blob.
        """
        self.specifier = specifier
        self._sampling_rate = None
        self._num_samples = None
        self._offset = None
        self._scale = None
        self._output_physical_dimension = None
        self.unit_scale = 1.0

    @property
    def label(self) -> Label:
        return self._label

    @label.setter
    def label(self, v: Union[str, Label]):
        if not isinstance(v, Label):
            v = Label(v.strip())

        self._label = v

    @property
    def num_records(self) -> int:
        return self._num_records

    @num_records.setter
    def num_records(self, v: int):
        self._num_records = v

    @property
    def num_records(self) -> int:
        return self._num_records

    @num_records.setter
    def num_records(self, v: int):
        self._num_records = v

    @property
    def physical_minimum(self) -> float:
        return self._physical_minimum

    @physical_minimum.setter
    def physical_minimum(self, v: float):
        self._physical_minimum = v

    @property
    def physical_maximum(self) -> float:
        return self._physical_maximum

    @physical_maximum.setter
    def physical_maximum(self, v: float):
        self._physical_maximum = v

    @property
    def digital_minimum(self) -> int:
        return self._digital_minimum

    @digital_minimum.setter
    def digital_minimum(self, v: int):
        self._digital_minimum = v

    @property
    def digital_maximum(self) -> int:
        return self._digital_maximum

    @digital_maximum.setter
    def digital_maximum(self, v: int):
        self._digital_maximum = v

    @property
    def record_duration(self) -> int:
        return self._record_duration

    @record_duration.setter
    def record_duration(self, v: int):
        self._record_duration = v

    @property
    def num_samples_per_record(self) -> int:
        return self._num_samples_per_record

    @num_samples_per_record.setter
    def num_samples_per_record(self, v: int):
        self._num_samples_per_record = v

    @property
    def sampling_rate(self) -> int:
        if self._sampling_rate is None:
            self._sampling_rate = self.num_samples_per_record / \
                                  self.record_duration  # ignore: type

        return self._sampling_rate

    @property
    def num_samples(self) -> int:
        if self._num_samples is None:
            self._num_samples = self.num_samples_per_record * self.num_records

        return self._num_samples

    @property
    def channel_type(self) -> str:
        return self._channel_type

    @channel_type.setter
    def channel_type(self, v: str):
        self._channel_type = v

    @property
    def type(self) -> str:
        """channel type from label"""
        return self.label.type

    @property
    def physical_dimension(self) -> str:
        return self._physical_dimension

    @physical_dimension.setter
    def physical_dimension(self, v: str):
        self._physical_dimension = v.strip()

    @property
    def output_physical_dimension(self) -> str:
        return self._output_physical_dimension \
               if self._output_physical_dimension \
               else self.physical_dimension

    @output_physical_dimension.setter
    def output_physical_dimension(self, v: str):
        self._output_physical_dimension = v
        self.unit_scale = convert_units(
            self.physical_dimension, self._output_physical_dimension)

    @property
    def prefiltering(self) -> str:
        return self._prefiltering

    @prefiltering.setter
    def prefiltering(self, v: str):
        self._prefiltering = v

    @property
    def reserved(self) -> str:
        return self._reserved

    @reserved.setter
    def reserved(self, v: str):
        self._reserved = v

    @property
    def scale(self) -> float:
        if self._scale is None:
            self._scale = (self.physical_maximum - self.physical_minimum) / \
                (self.digital_maximum - self.digital_minimum)

        return self._scale

    @property
    def offset(self) -> float:
        if self._offset is None:
            self._offset = self.physical_maximum / self.scale \
                           - self.digital_maximum  # pyright: disable

        return self._offset

    def digital2physical(self, data: np.ndarray, dtype=default_dtype,
                         specifier=None) -> np.ndarray:
        s = self.specifier if specifier is None else specifier
        assert s is not None, "channel index for edf record column missing"
        return dtype(self.unit_scale) * dtype(self.scale) \
            * (data[s].astype(dtype) + dtype(self.offset))

    def as_bytes(self, key: str, num_bytes: int = None) -> bytes:
        """Converts `str` representation of self.key to `bytes` instance"""
        fstring = "{:<%i}" % num_bytes if num_bytes else "{}"
        return bytes(fstring.format(getattr(self, key)), 'latin1')

    def to_bytes(self, key: str, typ=str) -> bytes:
        att = getattr(self, key)
        b = bytes(att, 'latin1') if typ is str else bytes(att)
        return b

    def to_string_list(self) -> List[str]:
        return [
            "{}: {}".format(key, val)
            for key, val in self.__dict__.items()
        ]

    def __str__(self) -> str:
        return '\n'.join(self.to_string_list())

    def _repr_html_(self) -> str:
        return ''.join(['<p>%s</p>' % s for s in self.to_string_list()])

    def check_compatible(self, other):
        for prop in ('sampling_rate', 'output_physical_dimension'):
            assert getattr(self, prop) == getattr(other, prop), \
                "'%s' and '%s' differ in '%s'" % (
                    self.label, other.label, prop)

    def __sub__(self, other):
        return ChannelDifference(self, other)
