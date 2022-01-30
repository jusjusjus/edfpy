from os import SEEK_SET
from typing import List, Iterable
from contextlib import contextmanager

import numpy as np

from .channel_fields import ChannelFields


def read_blob(filish, offset: int, record_lengths: List[int]):
    memarr = np.memmap(filish, dtype='<i2', mode='r', offset=offset)
    pos = np.cumsum([0] + record_lengths).astype(int)
    memarr.shape = (-1, pos[-1])
    locs = zip(pos[:-1], pos[1:])
    return [memarr[:, i:j].flatten() for i, j in locs]


def write_blob(file, channels: List[ChannelFields]):
    pass


class Blob:

    _bytes_per_sample = 2

    def __init__(self, file, records: int, samples_per_record: int,
                 channel_locs: List[int], offset: int):
        self._file = file
        self.keep_open = not isinstance(self._file, str)
        self.samples_per_record = samples_per_record
        self.records = records
        self.channel_locs = list(zip(channel_locs[:-1], channel_locs[1:]))
        self.offset = offset
        self.dtype = '<i%i' % self._bytes_per_sample

    @contextmanager
    def file(self):
        """return open file
        Use by creating a context:
        ```
            with self.file() as fo:
                fo.read() ..
        ```
        """
        try:
            fo = self._file if self.keep_open else open(self._file, 'rb')
            yield fo
        finally:
            if not self.keep_open:
                fo.close()

    def __getitem__(self, sl: slice) -> List[np.ndarray]:
        """Return data contained in the records of `sl`.

        Returned data is a by-channel list of all datapoints
        contained in the sliced records.  Size may differ for each
        channel depending on the sampling rate.
        """
        assert sl.step is None, "We don't resample like that."
        n = self.samples_per_record
        bytes_per_record = self._bytes_per_sample * n
        start = 0 if sl.start is None else sl.start
        stop = self.records if sl.stop is None else sl.stop
        ds = stop - start
        offset = bytes_per_record * start + self.offset
        readsize = bytes_per_record * ds
        shp = (ds, n)
        with self.file() as fo:
            fo.seek(offset, SEEK_SET)
            data = np.frombuffer(fo.read(readsize),
                                 dtype=self.dtype).reshape(shp)

        return [data[:, u:v].flatten() for u, v in self.channel_locs]

    def read(self, channel_indices: Iterable[int] = None) -> bytes:
        idx = channel_indices if channel_indices else np.arange(
            len(self.channel_locs))
        shp = (self.records, self.samples_per_record)
        with self.file() as fo:
            fo.seek(self.offset, SEEK_SET)
            data = np.frombuffer(fo.read(), dtype=self.dtype).reshape(shp)

        blob = np.concatenate([
            data[:, u:v] for i, (u, v) in enumerate(self.channel_locs)
            if i in idx
        ], axis=1)
        return blob.tostring()

    def __del__(self):
        if not isinstance(self._file, str):
            self._file.close()
