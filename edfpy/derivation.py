from typing import Dict, List

import numpy as np

from .channel_base import ChannelBase
from .label import Label


class Derivation(ChannelBase):
    operations = {
        '+': lambda l, r: l + r,
        '-': lambda l, r: l - r,
    }

    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.label, operation = left.label.derive(right.label)
        self.op = self.operations[operation]

    def __getitem__(self, sli: slice) -> np.ndarray:
        """return a slice of the derivation"""
        left = self.left[sli]
        right = self.right[sli]
        return self.op(left, right)

    def from_dict(self, signals: Dict[Label, np.ndarray]) -> np.ndarray:
        left = self.left.from_dict(signals)
        right = self.right.from_dict(signals)
        return self.op(left, right)

    @property
    def channel_type(self):
        return self.left.channel_type

    @property
    def physical_dimension(self) -> str:
        return self.left.physical_dimension

    @property
    def num_samples_per_record(self):
        return self.left.num_samples_per_record

    @property
    def children(self) -> List[Label]:
        children = self.left.children
        children.extend(self.right.children)
        return children

    def derive(self, other: ChannelBase) -> ChannelBase:
        if not self.is_compatible(other):
            raise ValueError(f"cannot derive {self} and {other}")

        return Derivation(self, other)
