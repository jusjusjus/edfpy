from typing import List, Dict, Iterable
from datetime import datetime
from itertools import product
import numpy as np
from .blob import read_blob
from .label import Label
from .header import Header
from .channel import Channel


class Reader:
    def __init__(self, header: Header, channels: List[Channel]):
        """initialize reader with a filepath"""
        self.header = header
        self.basic_labels = [c.label for c in channels]
        self.channel_by_label = {c.label: c for c in channels}
        self.derivation_by_label = {
            k: v for k, v in self.channel_by_label.items()
        }
        self.compute_derivations()

    @classmethod
    def open(cls, filepath: str) -> 'Reader':
        with open(filepath, 'rb') as fp:
            header = Header.read(fp)
            channels = Channel.read(fp, header.num_channels)

        offset = header.num_header_bytes
        record_lengths = [c.num_samples_per_record for c in channels]
        blob_slices = read_blob(filepath, offset, record_lengths)
        for channel, blob_slice in zip(channels, blob_slices):
            channel.signal = blob_slice

        return cls(header, channels)

    def compute_derivations(self):
        channels = list(self.derivation_by_label.values())
        for left, right in product(channels, channels):
            if left is right or not left.is_compatible(right):
                continue

            derivation = left.derive(right)
            if derivation.label not in self.derivation_by_label:
                self.derivation_by_label[derivation.label] = derivation

    @property
    def labels(self):
        return list(self.derivation_by_label.keys())

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
        labels1 = list(map(Label, labels)) if labels else self.basic_labels
        required_labels = self.required_from_requested(labels1)
        rd = self.header.record_duration
        signals = {}
        for label in required_labels:
            channel = self.channel_by_label[label]
            sr = channel.num_samples_per_record / rd
            a = int(np.round(t0 * sr))
            b = int(np.round(t1 * sr))
            signals[label] = channel[a:b]

        return {
            ll: self.derivation_by_label[ll].from_dict(signals)
            for ll in labels1
        }

    def required_from_requested(self, labels: List[Label]) -> Iterable[Label]:
        """returns the labels required to construct the requested signals"""
        for label in labels:
            yield from self.derivation_by_label[label].children
