
import logging
import numpy as np
from os import SEEK_SET
from struct import Struct
from .notation import Label
from datetime import datetime


default_dtype = np.float32


class Header:

    logger = logging.getLogger(name='Header')

    _fields = [
        ('version'         , str  , 8 ),
        ('patient_id'      , str  , 80),
        ('recording_id'    , str  , 80),
        ('startdate'       , str  , 8 ),
        ('starttime'       , str  , 8 ),
        ('num_header_bytes', int  , 8 ),
        ('reserved'        , str  , 44),
        ('num_records'     , int  , 8 ),
        ('record_duration' , float, 8 ),
        ('num_channels'    , int  , 4 )
    ]

    # format_str = ''.join(str(size) + 's' for _, _, size in fields_rec.bytesize)
    _format_str = '8s80s80s8s8s8s44s8s8s4s'

    def __init__(self, *args, **kwargs):
        self.datetime_changed = True
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def startdate(self):
        """Local start date of the recording"""
        return self._startdate
    
    @startdate.setter
    def startdate(self, v):
        self.datetime_changed = True
        self._startdate = self.normalize(str, v)

    @property
    def starttime(self):
        """Local start time of the recording"""
        return self._starttime
    
    @starttime.setter
    def starttime(self, v):
        self.datetime_changed = True
        self._starttime = self.normalize(str, v)

    @property
    def version(self):
        return self._version
    
    @version.setter
    def version(self, v):
        self._version = self.normalize(str, v)

    @property
    def patient_id(self):
        return self._patient_id
    
    @patient_id.setter
    def patient_id(self, v):
        self._patient_id = self.normalize(str, v)

    @property
    def recording_id(self):
        return self._recording_id
    
    @recording_id.setter
    def recording_id(self, v):
        self._recording_id = self.normalize(str, v)

    @property
    def reserved(self):
        return self._reserved
    
    @reserved.setter
    def reserved(self, v):
        self._reserved = self.normalize(str, v)

    @staticmethod
    def normalize(typ, v):
        if isinstance(v, str):
            v = v.strip('\x00')
        elif isinstance(v, bytes):
            v = v.strip(b'\x00')
        else:
            AttributeError("Unknown type")
        if typ is str:
            if isinstance(v, bytes):
                try:    v = str(v, 'ascii')
                except: v = str(v, 'latin1')
        else:
            v = typ(v)
        return v

    @property
    def startdatetime(self):
        if self.datetime_changed:
            try:
                self._startdatetime = datetime.strptime(
                    self.startdate + "-" + self.starttime, "%d.%m.%y-%H.%M.%S"
                )
            except: # sometimes the day and month are switched
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
        for field, typ, size in ChannelHeader._fields:
            num_bytes = size * nc
            _format_str = (str(size) + "s") * nc
            data = fo.read(num_bytes)
            values = Struct(_format_str).unpack(data)
            for i, val in enumerate(values):
                val = self.normalize(typ, val)
                setattr(channels[i], field, val)
            offset += num_bytes
        assert offset == self.num_header_bytes, 'invalid header'

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
        self.sampling_rate_by_channel = np.array([
            channel.sampling_rate
            for channel in self.channels
        ])
        self.channel_by_label = {c.label : c for c in channels}

    @classmethod
    def read_file(cls, filename):
        fo = cls.open_if_string(filename, 'rb')
        fo.seek(0, SEEK_SET)

        data = fo.read(256)
        values = Struct(cls._format_str).unpack(data)
        values = {
            name: cls.normalize(typ, value)
            for value, (name, typ, num_bytes) in zip(values, cls._fields)
        }

        instance = cls(**values)
        offset = instance._read_channels(fo)
        instance.set_blob(fo)
        return instance

    @classmethod
    def as_bytes(cls, val):
        """Converts the `str` representation of value `val` to a `bytes` instance."""
        return bytes(str(val), 'latin1')

    def to_bytes(self):
        # Main header
        ret = [
            self.as_bytes(getattr(self, key))
            for key, _, _ in self._fields
        ]
        # Channel headers
        channel_format_str = ''
        for key, _, size in ChannelHeader._fields:
            channel_format_str += (str(size)+'s')*self.num_channels
            ret += [
                self.as_bytes(getattr(channel, key))
                for channel in self.channels
            ]
        return ret, self._format_str + channel_format_str

    def write_file(self, filename):
        fo = self.open_if_string(filename, 'wb')
        blob, format_str = self.to_bytes()
        # print(len(blob), format_str)
        packed = Struct(format_str).pack(*blob)
        fo.seek(0, SEEK_SET)
        fo.write(packed)
        if isinstance(filename, str):
            fo.close()

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
        return ''.join(['<p>%s</p>'%s for s in self.to_string_list()])



class ChannelHeader:

    logger = logging.getLogger(name='ChannelHeader')

    _fields = [
        ('label'                 , str  , 16),
        ('channel_type'          , str  , 80),
        ('physical_dimension'    , str  , 8 ),
        ('physical_minimum'      , float, 8 ),
        ('physical_maximum'      , float, 8 ),
        ('digital_minimum'       , int  , 8 ),
        ('digital_maximum'       , int  , 8 ),
        ('prefiltering'          , str  , 80),
        ('num_samples_per_record', int  , 8 ),
        ('reserved'              , str  , 32)
    ]

    def __init__(self, specifier):
        """
        Arguments:
            specifier (optional) : specifies the channel construction,
            typically the reference index in a data blob.
        """
        self.specifier = specifier
        self._sampling_rate = None
        self._num_samples = None
        self._offset = None
        self._scale = None
        pass

    @property
    def label(self):
        return self._label
    
    @label.setter
    def label(self, v):
        if not isinstance(v, Label):
            v = Label(v.strip())
        self._label = v

    @property
    def sampling_rate(self):
        if self._sampling_rate is None:
            self._sampling_rate = self.num_samples_per_record / self.record_duration
        return self._sampling_rate
    
    @property
    def num_samples(self):
        if self._num_samples is None:
            self._num_samples = self.num_samples_per_record * self.num_records
        return self._num_samples

    @property
    def channel_type(self):
        return self._channel_type
    
    @channel_type.setter
    def channel_type(self, v):
        self._channel_type = v

    @property
    def physical_dimension(self):
        return self._physical_dimension
    
    @physical_dimension.setter
    def physical_dimension(self, v):
        self._physical_dimension = v

    @property
    def prefiltering(self):
        return self._prefiltering
    
    @prefiltering.setter
    def prefiltering(self, v):
        self._prefiltering = v

    @property
    def reserved(self):
        return self._reserved
    
    @reserved.setter
    def reserved(self, v):
        self._reserved = v

    @property
    def scale(self):
        if self._scale is None:
            self._scale  = (self.physical_maximum - self.physical_minimum) / \
                           (self.digital_maximum  - self.digital_minimum)
        return self._scale
    
    @property
    def offset(self):
        if self._offset is None:
            self._offset = self.physical_maximum / self.scale - self.digital_maximum
        return self._offset

    def digital2physical(self, data, dtype=default_dtype, specifier=None):
        s = self.specifier if specifier is None else specifier
        assert s is not None
        return dtype(self.scale)*(data[s].astype(dtype) + dtype(self.offset))

    def to_bytes(self, key):
        att = getattr(self, key)
        if typ is str:
            b = bytes(att, 'latin1')
        else:
            b = bytes(att)
        return b

    def to_string_list(self):
        return [
            "{}: {}".format(key, val)
            for key, val in self.__dict__.items()
        ]

    def __str__(self):
        return '\n'.join(self.to_string_list())

    def _repr_html_(self):
        return ''.join(['<p>%s</p>'%s for s in self.to_string_list()])
