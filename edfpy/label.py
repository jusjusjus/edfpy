from typing import Optional, Tuple

from .cached_property import cached_property


class Label(str):
    @property
    def left(self) -> Optional[str]:
        return self.parts[0]

    @cached_property
    def right(self) -> Optional[str]:
        return self.parts[1]

    @cached_property
    def parts(self):
        parts = self.split('-')
        if len(parts) == 1:
            return parts + [None]
        elif parts[0] == '':
            parts[0] = None

        return parts

    def derive(self, other: 'Label') -> Tuple['Label', str]:
        if not self.is_compatible(other):
            raise ValueError(f"Unable to derive {self} with {other}")

        try:
            return self + other, '+'
        except ValueError:
            return self - other, '-'

    def __add__(self, other: 'Label') -> 'Label':  # type: ignore
        if self.right == other.left:
            return self.from_channels(self.left, other.right)
        elif self.left == other.right:
            return self.from_channels(other.left, self.right)

        raise ValueError(f"Can't add {self} and {other}")

    def __sub__(self, other: 'Label') -> 'Label':
        if self.left == other.left:
            return self.from_channels(other.right, self.right)
        elif self.right == other.right:
            return self.from_channels(self.left, other.left)

        raise ValueError(f"Can't subtract {other} from {self}")

    def is_compatible(self, o: 'Label') -> bool:
        p = self.parts
        return o.left in p or o.right in p

    def __neg__(self):
        return self.from_channels(self.right, self.left)

    @classmethod
    def from_channels(cls, c1: Optional[str], c2: Optional[str]) -> 'Label':
        left: str = c1 or ''
        right: str = f"-{c2}" if c2 else ''
        return cls(f"{left}{right}")
