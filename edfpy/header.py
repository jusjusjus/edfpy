from io import SEEK_SET
from struct import Struct
from typing import BinaryIO
from datetime import datetime

from .cached_property import cached_property
from .field import Field, normalize, serialize


class Header:
    fields = [
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
    format_str = '8s80s80s8s8s8s44s8s8s4s'
    # _num_header_bytes = sum(field.size for field in fields)
    default_num_header_bytes = 256

    @property
    def version(self) -> str:
        return self._version

    @version.setter
    def version(self, v: str):
        self._version = normalize(str, v)

    @property
    def patient_id(self) -> str:
        return self._patient_id

    @patient_id.setter
    def patient_id(self, v: str):
        self._patient_id = normalize(str, v)

    @property
    def recording_id(self) -> str:
        return self._recording_id

    @recording_id.setter
    def recording_id(self, v: str):
        self._recording_id = normalize(str, v)

    @property
    def startdate(self) -> str:
        """Local start date of the recording"""
        return self._startdate

    @startdate.setter
    def startdate(self, v: str):
        self._startdate = normalize(str, v)

    @property
    def starttime(self) -> str:
        """Local start time of the recording"""
        return self._starttime

    @starttime.setter
    def starttime(self, v: str):
        self._starttime = normalize(str, v)

    @property
    def num_header_bytes(self) -> int:
        return self._num_header_bytes

    @num_header_bytes.setter
    def num_header_bytes(self, v: int):
        self._num_header_bytes = v

    @property
    def reserved(self) -> str:
        return self._reserved

    @reserved.setter
    def reserved(self, v: str):
        self._reserved = normalize(str, v)

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
    def num_channels(self) -> int:
        """returns seconds per record"""
        return self._num_channels

    @num_channels.setter
    def num_channels(self, v: int):
        self._num_channels = v

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            getattr(type(self), k).fset(self, v)

    @cached_property
    def startdatetime(self) -> datetime:
        datetime_str = f"{self.startdate}-{self.starttime}"
        try:
            return datetime.strptime(datetime_str, '%d.%m.%y-%H.%M.%S')
        except BaseException:
            # sometimes the day and month are switched
            return datetime.strptime(datetime_str, '%m.%d.%y-%H.%M.%S')

    @classmethod
    def read(cls, file: BinaryIO):
        data = file.read(cls.default_num_header_bytes)
        values = Struct(cls.format_str).unpack(data)
        named_content = {
            field.name: normalize(field.type, value)
            for field, value in zip(cls.fields, values)
        }
        return cls(**named_content)

    def write(self, file: BinaryIO):
        blob = [serialize(getattr(self, field.name), field.size)
                for field in self.fields]
        packed = Struct(self.format_str).pack(*blob)
        file.seek(0, SEEK_SET)
        file.write(packed)
