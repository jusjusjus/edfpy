from os import SEEK_SET
from typing import Optional
from logging import getLogger
from datetime import datetime

import numpy as np

from .header_fields import HeaderFields
from .channel_header import ChannelHeader
from .channel_difference import ChannelDifference


class Header(HeaderFields):
    logger = getLogger(name='Header')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._startdatetime: Optional[datetime] = None

    @property
    def startdatetime(self) -> datetime:
        if not self._startdatetime:
            try:
                self._startdatetime = datetime.strptime(
                    self.startdate + "-" + self.starttime, "%d.%m.%y-%H.%M.%S"
                )
            except BaseException:  # sometimes the day and month are switched
                self.logger.info("Time format seems to be MON.DAY.YEAR")
                self._startdatetime = datetime.strptime(
                    self.startdate + "-" + self.starttime, "%m.%d.%y-%H.%M.%S"
                )

        return self._startdatetime

    def build_channel_differences(self, depth: int = 1):
        for _ in range(depth):
            self._build_channel_differences()

    def add_synonym(self, synonym: str, label: str):
        """add a `synonym` for a channel `label`"""
        channel = self.channel_by_label[label]
        sampling_rate = self.sampling_rate_by_label[label]
        self.channel_by_label[synonym] = channel
        self.sampling_rate_by_label[synonym] = sampling_rate

    def _build_channel_differences(self):
        channels = list(self.channel_by_label.values())
        for index, left in enumerate(channels):
            for right in channels[index + 1:]:
                try:
                    self.append_channel(left - right)
                    self.append_channel(right - left)
                except (AssertionError, TypeError) as e:
                    self.logger.info(
                        "In Header.build_channel_differences: %s" % e)

    def append_channel(self, channel: ChannelDifference):
        """append channel to channel dictionaries"""
        self.channel_by_label[channel.label] = channel
        self.sampling_rate_by_label[channel.label] = channel.sampling_rate

    @classmethod
    def read_file(cls, filename: str, keep_open: bool = True):
        fo = cls.open_if_string(filename, 'rb')
        fo.seek(0, SEEK_SET)
        instance = cls.read(fo)
        instance._read_channels(fo)
        if keep_open:
            instance.set_blob(fo)
        else:
            fo.close()
            instance.set_blob(filename)

        return instance

    @staticmethod
    def open_if_string(f, mode):
        if isinstance(f, str):
            fo = open(f, mode)
        else:
            fo = f

        for m in ('read', 'seek'):
            assert hasattr(fo, m), "Missing property in \
                    file ['{}', '{}', '{}']".format(m, f, fo)

        return fo

    def _read_channels(self, file):
        self.channels = ChannelHeader.read(file, self.num_channels)
        # Add some redundance for fast access
        for key in ('record_duration', 'num_records'):
            att = getattr(self, key)
            for channel in self.channels:
                setattr(channel, key, att)

        self.samples_by_channel = np.array([
            channel.num_samples
            for channel in self.channels
        ])
        self.samples_per_record_by_channel = np.array([
            channel.num_samples_per_record
            for channel in self.channels
        ])
        self.sampling_rates = np.array([
            channel.sampling_rate
            for channel in self.channels
        ])
        self.sampling_rate_by_label = {
            channel.label: channel.sampling_rate
            for channel in self.channels
        }
        self.channel_by_label = {c.label: c for c in self.channels}

    def set_blob(self, fo):
        pass

    def write_file(self, filename: str, close=True, channels=None):
        fo = self.open_if_string(filename, 'wb')
        fo.seek(0, SEEK_SET)
        self.write(fo)
        ChannelHeader.write(fo, channels)
        if isinstance(filename, str) and close:
            fo.close()

        return fo

    def to_string_list(self):
        return [
            "{}: {}".format(key, val)
            for key, val in self.__dict__.items()
        ]

    def __str__(self):
        return '\n'.join(self.to_string_list())

    def _repr_html_(self):
        return ''.join(['<p>%s</p>' % s for s in self.to_string_list()])
