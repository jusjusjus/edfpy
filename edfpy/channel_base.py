from .label import Label
from .field import normalize


class ChannelBase:
    @property
    def label(self) -> Label:
        return self._label

    @label.setter
    def label(self, v: str):
        n = normalize(str, v)
        self._label = Label(n)

    @property
    def physical_dimension(self) -> str:
        raise NotImplementedError

    @property
    def num_samples_per_record(self) -> int:
        raise NotImplementedError

    def is_compatible(self, other: 'ChannelBase') -> bool:
        raise NotImplementedError
