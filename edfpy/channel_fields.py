from typing import List, BinaryIO
from struct import Struct

from .field import Field, normalize, serialize


class ChannelFields:
    fields = [
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

    def __init__(self, specifier: int, **kwargs):
        self.specifier = specifier
        for k, v in kwargs.items():
            try:
                # Accessing `prop.setter` through class property
                getattr(type(self), k).fset(self, v)
            except AttributeError:
                setattr(self, k, v)

    @property
    def label(self) -> str:
        return self._label

    @label.setter
    def label(self, v: str):
        self._label = normalize(str, v)

    @property
    def channel_type(self) -> str:
        return self._channel_type

    @channel_type.setter
    def channel_type(self, v: str):
        self._channel_type = normalize(str, v)

    @property
    def physical_dimension(self) -> str:
        return self._physical_dimension

    @physical_dimension.setter
    def physical_dimension(self, v: str):
        self._physical_dimension = normalize(str, v)

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
    def prefiltering(self) -> str:
        return self._prefiltering

    @prefiltering.setter
    def prefiltering(self, v: str):
        self._prefiltering = normalize(str, v)

    @property
    def num_samples_per_record(self) -> int:
        return self._num_samples_per_record

    @num_samples_per_record.setter
    def num_samples_per_record(self, v: int):
        self._num_samples_per_record = v

    @property
    def reserved(self) -> str:
        return self._reserved

    @reserved.setter
    def reserved(self, v: str):
        self._reserved = normalize(str, v)

    @classmethod
    def read(cls, file: BinaryIO, num_channels: int) -> List['ChannelFields']:
        channels = [cls(i) for i in range(num_channels)]
        for field in cls.fields:
            data = file.read(field.size * num_channels)
            format_str = (str(field.size) + "s") * num_channels
            values = Struct(format_str).unpack(data)
            normalized = (normalize(field.type, v) for v in values)
            for c, v in zip(channels, normalized):
                setattr(c, field.name, v)

        return channels

    @classmethod
    def write(cls, file: BinaryIO, channels: List['ChannelFields']):
        serialized = b''
        for field in cls.fields:
            serialized += b''.join([
                serialize(getattr(channel, field.name), field.size)
                for channel in channels
            ])

        file.write(serialized)
