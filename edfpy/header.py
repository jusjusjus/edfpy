from os import SEEK_SET
from struct import Struct
from logging import getLogger
from datetime import datetime

import numpy as np

from .field import Field
from .channel_header import ChannelHeader
from .channel_difference import ChannelDifference


class Header:

    logger = getLogger(name='Header')

    _fields = [
        Field('version', str, 8),
        Field('patient_id', str, 80),
        Field('recording_id', str, 80),
        Field('startdate', str, 8),
        Field('starttime', str, 8),
        Field('num_header_bytes', int, 8),
        Field('reserved', str, 44),
        Field('num_records', int, 8),
        Field('record_duration', float, 8),
        Field('num_channels', int, 4)
    ]

    # format_str = ''.join(str(size) + 's'
    #                      for _, _, size in fields_rec.bytesize)

    _format_str = '8s80s80s8s8s8s44s8s8s4s'
    # _num_header_bytes = sum(c for _,_,c in _fields)
    _num_header_bytes = 256

    def __init__(self, *args, **kwargs):
        self.datetime_changed = True
        for k, v in kwargs.items():
            try:
                # Accessing `prop.setter` through class property
                getattr(type(self), k).fset(self, v)
            except AttributeError:
                setattr(self, k, v)

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

    def add_synonym(self, synonym: str, label: str):
        """add a `synonym` for a channel `label`"""
        channel = self.channel_by_label[label]
        sampling_rate = self.sampling_rate_by_label[label]
        self.channel_by_label[synonym] = channel
        self.sampling_rate_by_label[synonym] = sampling_rate

    def build_channel_differences(self, depth: int = 1):
        for _ in range(depth):
            self._build_channel_differences()

    @property
    def num_records(self) -> int:
        """returns number of records"""
        return self._num_records

    @num_records.setter
    def num_records(self, v: int):
        self._num_records = v

    @property
    def record_duration(self) -> int:
        """returns seconds per record"""
        return self._record_duration

    @record_duration.setter
    def record_duration(self, v: int):
        self._record_duration = v

    @property
    def startdate(self) -> str:
        """Local start date of the recording"""
        return self._startdate

    @startdate.setter
    def startdate(self, v: str):
        self.datetime_changed = True
        self._startdate = self.normalize(str, v)

    @property
    def starttime(self) -> str:
        """Local start time of the recording"""
        return self._starttime

    @starttime.setter
    def starttime(self, v: str):
        self.datetime_changed = True
        self._starttime = self.normalize(str, v)

    @property
    def version(self) -> str:
        return self._version

    @version.setter
    def version(self, v: str):
        self._version = self.normalize(str, v)

    @property
    def patient_id(self) -> str:
        return self._patient_id

    @patient_id.setter
    def patient_id(self, v: str):
        self._patient_id = self.normalize(str, v)

    @property
    def recording_id(self) -> str:
        return self._recording_id

    @recording_id.setter
    def recording_id(self, v: str):
        self._recording_id = self.normalize(str, v)

    @property
    def reserved(self) -> str:
        return self._reserved

    @reserved.setter
    def reserved(self, v: str):
        self._reserved = self.normalize(str, v)

    @staticmethod
    def normalize(typ, v):
        if isinstance(v, str):
            v = v.strip('\x00').strip(' ')
        elif isinstance(v, bytes):
            v = v.strip(b'\x00')
        else:
            AttributeError("Unknown type")

        if typ is str:
            if isinstance(v, bytes):
                try:
                    v = str(v, 'ascii')
                except BaseException:
                    v = str(v, 'latin1')

        else:
            v = typ(v)

        return v

    @property
    def startdatetime(self) -> datetime:
        if self.datetime_changed:
            try:
                self._startdatetime = datetime.strptime(
                    self.startdate + "-" + self.starttime, "%d.%m.%y-%H.%M.%S"
                )
            except BaseException:  # sometimes the day and month are switched
                self.logger.info("Time format seems to be MON.DAY.YEAR")
                self._startdatetime = datetime.strptime(
                    self.startdate + "-" + self.starttime, "%m.%d.%y-%H.%M.%S"
                )

            self.datetime_changed = False

        return self._startdatetime

    def _read_channels(self, fo):
        offset = 256
        nc = self.num_channels
        channels = [ChannelHeader(i) for i in range(nc)]
        for field in ChannelHeader._fields:
            num_bytes = field.size * nc
            _format_str = (str(field.size) + "s") * nc
            data = fo.read(num_bytes)
            values = Struct(_format_str).unpack(data)
            normalized = (self.normalize(field.type, v) for v in values)
            for c, v in zip(channels, normalized):
                setattr(c, field.name, v)
            offset += num_bytes

        assert offset == self.num_header_bytes, f" \
            invalid header of size {offset} [{self.num_header_bytes}]"

        # Add some redundance for fast access
        for key in ('record_duration', 'num_records'):
            att = getattr(self, key)
            for channel in channels:
                setattr(channel, key, att)

        self.channels = channels
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
        self.channel_by_label = {c.label: c for c in channels}

    def set_blob(self, fo):
        pass

    @classmethod
    def read_file(cls, filename: str, keep_open: bool = True):
        fo = cls.open_if_string(filename, 'rb')
        fo.seek(0, SEEK_SET)

        data = fo.read(256)
        values = Struct(cls._format_str).unpack(data)
        named_content = {
            field.name: cls.normalize(field.type, value)
            for field, value in zip(cls._fields, values)
        }
        instance = cls(**named_content)
        instance._read_channels(fo)
        if keep_open:
            instance.set_blob(fo)
        else:
            fo.close()
            instance.set_blob(filename)

        return instance

    def as_bytes(self, key: str, num_bytes: int = None):
        """Converts `str` representation of `self.key` to `bytes` instance"""
        fstring = "{:<%i}" % num_bytes if num_bytes else "{}"
        return bytes(fstring.format(getattr(self, key)), 'latin1')

    @property
    def num_header_bytes(self) -> int:
        return self._num_header_bytes + \
               self.num_channels * ChannelHeader._num_header_bytes

    @num_header_bytes.setter
    def num_header_bytes(self, v: int):
        pass

    def to_bytes(self, channels=None):
        if channels is not None:
            channels = sorted([self.channel_by_label[c] for c in channels],
                              key=lambda c: c.specifier)
        else:
            channels = self.channels

        # Temporarily change `self.num_channels`
        tmp_num_ch = self.num_channels
        self.num_channels = len(channels)
        # Main header
        ret = [
            self.as_bytes(field.name, field.size)
            for field in self._fields
        ]
        # Channel headers
        channel_format_str = ''
        for field in ChannelHeader._fields:
            channel_format_str += (str(field.size)+'s') * self.num_channels
            ret += [
                channel.as_bytes(field.name, num_bytes=field.size)
                for channel in channels
            ]

        # Change `self.num_channels` back to original
        self.num_channels = tmp_num_ch
        return ret, self._format_str + channel_format_str

    def write_file(self, filename: str, close=True, channels=None):
        fo = self.open_if_string(filename, 'wb')
        blob, format_str = self.to_bytes(channels=channels)
        packed = Struct(format_str).pack(*blob)
        fo.seek(0, SEEK_SET)
        fo.write(packed)
        if isinstance(filename, str) and close:
            fo.close()

        return fo

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

    def to_string_list(self):
        return [
            "{}: {}".format(key, val)
            for key, val in self.__dict__.items()
        ]

    def __str__(self):
        return '\n'.join(self.to_string_list())

    def _repr_html_(self):
        return ''.join(['<p>%s</p>' % s for s in self.to_string_list()])
