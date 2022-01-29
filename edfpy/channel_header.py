from typing import List, Union

import numpy as np

from .notation import Label, convert_units
from .channel_difference import ChannelDifference
from .channel_fields import ChannelFields

default_dtype = np.float32


class ChannelHeader(ChannelFields):

    def __init__(self, specifier, **kwargs):
        """
        Arguments:
            specifier: specifies the channel construction,
            typically the reference index in a data blob.
        """
        super().__init__(specifier, **kwargs)
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
    def num_records(self) -> int:
        return self._num_records

    @num_records.setter
    def num_records(self, v: int):
        self._num_records = v

    @property
    def type(self) -> str:
        """channel type from label"""
        return self.label.type

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
