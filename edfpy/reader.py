from typing import List
import logging
import numpy as np
from .header import Header
from .blob import Blob


class EDF(Header):

    logger = logging.getLogger(name='EDF')

    @property
    def duration(self):
        """Returns total duration of the recording in seconds."""
        return self.record_duration * self.num_records

    def get_digital_samples(self, t0=0.0, dt=None):
        """Return digital samples from `t0` to `t0+dt`."""
        sr = self.sampling_rates
        n = self.samples_per_record_by_channel
        if dt is None:
            dt = self.num_records*self.record_duration
        # start/stop samples per channel
        a = np.round(t0*sr).astype(int)
        b = np.round((t0+dt)*sr).astype(int)
        # start/stop record enclosing (min(a), max(b))
        A = np.floor(a/n).astype(int).min()
        B = np.ceil(b/n).astype(int).max()
        # relative start/stop of data read
        a1 = a - A*n
        b1 = b - B*n  # result is <= 0
        b1 = [None if b1_ == 0 else b1_ for b1_ in b1]
        # Read data and return result
        data = self.blob[A:B]
        return [d[l:r] for d, l, r in zip(data, a1, b1)]

    def get_physical_samples(self, t0: float = 0.0, dt: float = None,
                             channels: List[str] = None):
        """Return physical samples from `t0` to `t0+dt`

        Arguments:
        - t0 : start time
        - dt : time difference to read out
        - channels : contains the list of channel labels that shall be
          returned.  `None` returns all channels.

        Returns:`
            a dict by channel label of the numpy.arrays with the data.
        """
        data = self.get_digital_samples(t0, dt)
        if channels is None:
            return {c.label: c.digital2physical(data) for c in self.channels}
        else:
            # Returns a channel, but with a potentially different label
            return {
                c: self.channel_by_label[c].digital2physical(data)
                for c in channels if c in self.channel_by_label
            }

    def set_blob(self, fo):
        s = list(self.samples_per_record_by_channel)
        channel_locs = np.cumsum([0] + s).astype(int)
        samples_per_record = sum(s)
        self.blob = Blob(
            fo,
            self.num_records,
            samples_per_record,
            channel_locs,
            self.num_header_bytes
        )

    def write_file(self, filename, channels=None):
        fo = super().write_file(filename, close=False, channels=channels)
        idx = [i for i, c in enumerate(
            self.channels) if c.label in channels] if channels else None
        blob = self.blob.read(channel_indices=idx)
        fo.write(blob)
        if isinstance(filename, str):
            fo.close()
