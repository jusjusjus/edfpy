from .cached_property import cached_property


class Label(str):
    @property
    def left(self):
        return self.parts[0]

    @cached_property
    def right(self):
        return self.parts[1]

    @cached_property
    def parts(self):
        parts = self.split('-')
        if len(parts) == 1:
            return parts + [None]
        elif parts[0] == '':
            parts[0] = None

        return parts

    def reference(self, other):
        if self.left == other.right or self.right == other.left:
            return self + other
        elif self.left == other.left or self.right == other.right:
            return self - other

        raise ValueError(f"Can't reference {self} with {other}")

    def __add__(self, other):
        cls = type(self)
        if self.right == other.left:
            return cls.from_channels(self.left, other.right)
        elif self.left == other.right:
            return cls.from_channels(other.left, self.right)

        raise ValueError(f"Can't add {self} and {other}")

    def __sub__(self, other):
        cls = type(self)
        if self.left == other.left:
            return cls.from_channels(other.right, self.right)
        elif self.right == other.right:
            return cls.from_channels(self.left, other.left)

        raise ValueError(f"Can't subtract {other} from {self}")

    def has_common_part(self, o):
        p = self.parts
        return o.left in p or o.right in p

    def __invert__(self):
        return self.from_channels(self.right, self.left)

    @classmethod
    def from_channels(cls, c1, c2):
        left = c1 or ''
        right = f"-{c2}" if c2 else ''
        return cls(f"{left}{right}")
