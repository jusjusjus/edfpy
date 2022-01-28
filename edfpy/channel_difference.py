class ChannelDifference:

    def __init__(self, left, right):
        left.check_compatible(right)
        self.left = left
        self.right = right
        self.label = left.label-right.label

    def check_compatible(self, other):
        """check compatibility of left and right

        note that compatibility is transitive. left vs right already checked in
        `__init__`.
        """
        self.left.check_compatible(other)

    @property
    def type(self) -> str:
        return self.label.type

    @property
    def sampling_rate(self) -> int:
        return self.left.sampling_rate

    @property
    def physical_dimension(self) -> str:
        return self.left.physical_dimension

    def digital2physical(self, *args, **kwargs):
        return self.left.digital2physical(*args, **kwargs) \
            - self.right.digital2physical(*args, **kwargs)

    def __sub__(self, other):
        return ChannelDifference(self, other)

    @property
    def output_physical_dimension(self) -> str:
        return self.left.output_physical_dimension

    @output_physical_dimension.setter
    def output_physical_dimension(self, v: str):
        self.left.output_physical_dimension = v
        self.right.output_physical_dimension = v
