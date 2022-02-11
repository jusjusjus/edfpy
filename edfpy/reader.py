from typing import List, Dict, Iterable
from datetime import datetime
import numpy as np
from .blob import read_blob
from .label import Label
from .header import Header
from .channel import Channel


class Reader:
    def __init__(self, filepath: str):
        """initialize reader with a filepath"""
        self.filepath = filepath
        with open(filepath, 'rb') as fp:
            self.header = Header.read(fp)
            channels = Channel.read(fp, self.header.num_channels)

        self.channel_by_label = {c.label: c for c in channels}
        self.basic_labels = [c.label for c in channels]
        offset = self.header.num_header_bytes
        record_lengths = [c.num_samples_per_record for c in channels]
        blob_slices = read_blob(filepath, offset, record_lengths)
        for channel, blob_slice in zip(channels, blob_slices):
            channel.signal = blob_slice

    @property
    def duration(self) -> int:
        """returns recording duration in seconds"""
        return self.header.record_duration * self.header.num_records

    @property
    def startdatetime(self) -> datetime:
        """returns the time point of recording start"""
        return self.header.startdatetime

    def get_physical_samples(self, t0: float = 0.0, dt: float = None,
                             labels: List[str] = None) -> Dict[Label, np.ndarray]:  # noqa: E501
        """returns dict of samples by label from `t0` to `t0+dt`."""
        dt = dt or self.duration
        t1 = t0 + dt
        required_labels = self.required_from_requested(labels)
        rd = self.header.record_duration
        signals = {}
        for label in required_labels:
            channel = self.channel_by_label[label]
            sr = channel.num_samples_per_record / rd
            a = int(np.round(t0 * sr))
            b = int(np.round(t1 * sr))
            signals[label] = channel[a:b]

        return signals

    def required_from_requested(self,
                                labels: List[str] = None) -> Iterable[Label]:
        """returns the labels required to construct the requested"""
        if labels is None:
            return self.basic_labels

        return map(Label, labels)
