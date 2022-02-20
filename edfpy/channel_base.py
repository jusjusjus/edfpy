from typing import List, Dict

import numpy as np

from .label import Label
from .field import normalize


class ChannelBase:
    @property
    def label(self) -> Label:
        return self._label

    @label.setter
    def label(self, v: str):
        n = normalize(Label, v)
        self._label = n

    @property
    def children(self) -> List[Label]:
        raise NotImplementedError

    @property
    def physical_dimension(self) -> str:
        raise NotImplementedError

    @property
    def num_samples_per_record(self) -> int:
        raise NotImplementedError

    def is_compatible(self, other: 'ChannelBase') -> bool:
        compat_label = self.label.is_compatible(other.label)
        same_units = self.physical_dimension == other.physical_dimension
        same_sr = self.num_samples_per_record == other.num_samples_per_record
        return same_units and same_sr and compat_label

    def from_dict(self, signals_dict: Dict[Label, np.ndarray]) -> np.ndarray:
        raise NotImplementedError
