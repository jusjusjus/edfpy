import logging

import numpy as np

from .notation import Label, convert_units
from .channel_difference import ChannelDifference

default_dtype = np.float32


class ChannelHeader:

    logger = logging.getLogger(name='ChannelHeader')

    _fields = [
        ('label', str, 16),
        ('channel_type', str, 80),
        ('physical_dimension', str, 8),
        ('physical_minimum', float, 8),
        ('physical_maximum', float, 8),
        ('digital_minimum', int, 8),
        ('digital_maximum', int, 8),
        ('prefiltering', str, 80),
        ('num_samples_per_record', int, 8),
        ('reserved', str, 32)
    ]

    # _num_channel_header_bytes = sum(c for _,_,c in _fields)
    _num_header_bytes = 256

    def __init__(self, specifier):
        """
        Arguments:
            specifier (optional) : specifies the channel construction,
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
    def label(self):
        return self._label

    @label.setter
    def label(self, v):
        if not isinstance(v, Label):
            v = Label(v.strip())

        self._label = v

    @property
    def sampling_rate(self):
        if self._sampling_rate is None:
            self._sampling_rate = self.num_samples_per_record / \
                                  self.record_duration  # ignore: type

        return self._sampling_rate

    @property
    def num_samples(self):
        if self._num_samples is None:
            self._num_samples = self.num_samples_per_record * self.num_records

        return self._num_samples

    @property
    def channel_type(self):
        return self._channel_type

    @channel_type.setter
    def channel_type(self, v):
        self._channel_type = v

    @property
    def type(self):
        """channel type from label"""
        return self.label.type

    @property
    def physical_dimension(self):
        return self._physical_dimension

    @physical_dimension.setter
    def physical_dimension(self, v):
        self._physical_dimension = v.strip()

    @property
    def output_physical_dimension(self):
        return self._output_physical_dimension \
               if self._output_physical_dimension \
               else self.physical_dimension

    @output_physical_dimension.setter
    def output_physical_dimension(self, v):
        self._output_physical_dimension = v
        self.unit_scale = convert_units(
            self.physical_dimension, self._output_physical_dimension)

    @property
    def prefiltering(self):
        return self._prefiltering

    @prefiltering.setter
    def prefiltering(self, v):
        self._prefiltering = v

    @property
    def reserved(self):
        return self._reserved

    @reserved.setter
    def reserved(self, v):
        self._reserved = v

    @property
    def scale(self):
        if self._scale is None:
            self._scale = (self.physical_maximum - self.physical_minimum) / \
                (self.digital_maximum - self.digital_minimum)

        return self._scale

    @property
    def offset(self):
        if self._offset is None:
            self._offset = self.physical_maximum / self.scale \
                           - self.digital_maximum  # pyright: disable

        return self._offset

    def digital2physical(self, data, dtype=default_dtype, specifier=None):
        s = self.specifier if specifier is None else specifier
        assert s is not None, "channel index for edf record column missing"
        return dtype(self.unit_scale) * dtype(self.scale) \
            * (data[s].astype(dtype) + dtype(self.offset))

    def as_bytes(self, key, num_bytes=None):
        """Converts `str` representation of self.key to `bytes` instance"""
        fstring = "{:<%i}" % num_bytes if num_bytes else "{}"
        return bytes(fstring.format(getattr(self, key)), 'latin1')

    def to_bytes(self, key, typ=str):
        att = getattr(self, key)
        b = bytes(att, 'latin1') if typ is str else bytes(att)
        return b

    def to_string_list(self):
        return [
            "{}: {}".format(key, val)
            for key, val in self.__dict__.items()
        ]

    def __str__(self):
        return '\n'.join(self.to_string_list())

    def _repr_html_(self):
        return ''.join(['<p>%s</p>' % s for s in self.to_string_list()])

    def check_compatible(self, other):
        for prop in ('sampling_rate', 'output_physical_dimension'):
            assert getattr(self, prop) == getattr(other, prop), \
                "'%s' and '%s' differ in '%s'" % (
                    self.label, other.label, prop)

    def __sub__(self, other):
        return ChannelDifference(self, other)
