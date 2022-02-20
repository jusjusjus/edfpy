from typing import List, BinaryIO, Optional, Dict
from struct import Struct

import numpy as np

from .blob import BlobSlice
from .label import Label
from .field import Field, normalize, serialize
from .derivation import Derivation
from .channel_base import ChannelBase


class Channel(ChannelBase):
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

    def __init__(self, *args, **kwargs):
        self.signal: Optional[BlobSlice] = None
        for k, v in kwargs.items():
            getattr(type(self), k).fset(self, v)

    def __getitem__(self, sli: slice) -> np.ndarray:
        """return a slice of the signal"""
        if self.signal is None:
            raise RuntimeError(f"channel {self} uninitialized")

        scale = (self.physmax - self.physmin) / (self.digimax - self.digimin)
        offset = self.physmax / scale - self.digimax
        return scale * (self.signal[sli] + offset)

    def from_dict(self, signals: Dict[Label, np.ndarray]) -> np.ndarray:
        return signals[self.label]

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
        return self.physmin

    @physical_minimum.setter
    def physical_minimum(self, v: float):
        self.physmin = v

    @property
    def physical_maximum(self) -> float:
        return self.physmax

    @physical_maximum.setter
    def physical_maximum(self, v: float):
        self.physmax = v

    @property
    def digital_minimum(self) -> int:
        return self.digimin

    @digital_minimum.setter
    def digital_minimum(self, v: int):
        self.digimin = v

    @property
    def digital_maximum(self) -> int:
        return self.digimax

    @digital_maximum.setter
    def digital_maximum(self, v: int):
        self.digimax = v

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

    def derive(self, other: ChannelBase) -> Derivation:
        if not self.is_compatible(other):
            raise ValueError(f"cannot derive {self} and {other}")

        return Derivation(self, other)

    @property
    def children(self) -> List[Label]:
        return [self.label]

    @classmethod
    def read(cls, file: BinaryIO, num_channels: int) -> List['Channel']:
        channels = [cls() for _ in range(num_channels)]
        for field in cls.fields:
            data = file.read(field.size * num_channels)
            format_str = (str(field.size) + 's') * num_channels
            values = Struct(format_str).unpack(data)
            normalized = (normalize(field.type, v) for v in values)
            for c, v in zip(channels, normalized):
                setattr(c, field.name, v)

        return channels

    @classmethod
    def write(cls, file: BinaryIO, channels: List['Channel']):
        serialized = b''
        for field in cls.fields:
            serialized += b''.join([
                serialize(getattr(channel, field.name), field.size)
                for channel in channels
            ])

        file.write(serialized)
