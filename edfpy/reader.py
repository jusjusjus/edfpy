from datetime import datetime
import numpy as np
from .blob import read_blob
from .header import Header
from .channel import Channel


class Reader:
    def __init__(self, filepath: str):
        """read filepath"""
        self.filepath = filepath
        with open(filepath, 'rb') as fp:
            self.header = Header.read(fp)
            self.channels = Channel.read(fp, self.header.num_channels)

        offset = self.header.num_header_bytes
        record_lengths = [c.num_samples_per_record for c in self.channels]
        blob_slices = read_blob(filepath, offset, record_lengths)
        for channel, blob_slice in zip(self.channels, blob_slices):
            channel.signal = blob_slice

        self.sampling_rates = np.array([
            channel.num_samples_per_record for channel in self.channels
        ]) / self.header.record_duration

    @property
    def duration(self) -> int:
        """returns recording duration in seconds"""
        return self.header.record_duration * self.header.num_records

    @property
    def startdatetime(self) -> datetime:
        """returns the time point of recording start"""
        return self.header.startdatetime

    def get_physical_samples(self, t0: float = 0.0, dt: float = None):
        """Return digital samples from `t0` to `t0+dt`."""
        sr = self.sampling_rates
        dt = dt or self.duration
        A = np.round(t0 * sr).astype(int)
        B = np.round((t0 + dt) * sr).astype(int)
        return [c[a:b] for c, a, b in zip(self.channels, A, B)]
