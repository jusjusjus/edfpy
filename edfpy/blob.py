from typing import List, Tuple

import numpy as np


class BlobSlice:
    def __init__(self, blob: np.memmap, locs: Tuple[int, int]):
        self.blob = blob
        self.block_size = locs[1] - locs[0]
        self.length = blob.shape[0] * self.block_size
        self.locs = slice(*locs)

    def __getitem__(self, sl: slice) -> np.ndarray:
        if sl.step and sl.step != 1:
            raise ValueError('slicing only with step width 1')

        q = self.block_size
        i = sl.start if sl.start else 0
        j = sl.stop if sl.stop else self.length
        j = self.length + j if j < 0 else j
        A = i // q
        B = int(np.ceil(j / q))
        a = i - A * q
        b = j - B * q or None
        block = self.blob[A:B, self.locs].flatten()
        return block[a:b]

    def __eq__(self, other):
        return self[:] == other

    def __repr__(self):
        return f"BlobSlice({self[:]})"


def read_blob(file, offset: int, record_lengths: List[int]):
    memarr = np.memmap(file, dtype='<i2',  # type: ignore
                       mode='r', offset=offset)
    pos = np.cumsum([0] + record_lengths).astype(int)
    memarr.shape = (-1, pos[-1])
    locs = zip(pos[:-1], pos[1:])
    return [BlobSlice(memarr, loc) for loc in locs]


def write_blob(file, arrs: List[np.ndarray], record_lengths: List[int]):
    reshaped = [arr.reshape((-1, n)) for arr, n in zip(arrs, record_lengths)]
    blob = np.concatenate(reshaped, axis=1).tobytes()
    file.write(blob)
