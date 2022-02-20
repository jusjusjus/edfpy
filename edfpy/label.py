from typing import Optional, Tuple
from .cached_property import cached_property
from .notation import synonyms


class Label(str):
    def __init__(self, original: str):
        """initialize Label with `.original` storing input str"""
        self.original = original

    def __new__(cls, original: str):
        """normalize original input str in new instance"""
        normalized = cls.normalize(original)
        return super().__new__(cls, normalized)

    @classmethod
    def normalize(cls, original: str) -> str:
        split = original.replace('/', '-').upper().split(' ')
        label = split[1] if 1 < len(split) else split[0]
        synonym_tuple = (
            synonyms.get(part, part)
            for part in label.split('-')
        )
        return '-'.join(synonym_tuple)

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
            return self.construct(self.left, other.right)
        elif self.left == other.right:
            return self.construct(other.left, self.right)

        raise ValueError(f"Can't add {self} and {other}")

    def __sub__(self, other: 'Label') -> 'Label':
        if self.left == other.left:
            return self.construct(other.right, self.right)
        elif self.right == other.right:
            return self.construct(self.left, other.left)

        raise ValueError(f"Can't subtract {other} from {self}")

    def is_compatible(self, o: 'Label') -> bool:
        p = self.parts
        return o.left in p or o.right in p

    def __neg__(self):
        return self.construct(self.right, self.left)

    @classmethod
    def construct(cls, ls: Optional[str], rs: Optional[str]) -> 'Label':
        left: str = ls or ''
        right: str = f"-{rs}" if rs else ''
        return cls(f"{left}{right}")
