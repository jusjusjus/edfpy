from collections import namedtuple
from ..cached_property import cached_property
from .channel import Channel


Annotation = namedtuple('Annotation', 'start duration label')


class AnnotationChannel(Channel):

    sep_annotations = b'\x14\x00'  # after each annotation
    sep_timestamp = b'\x15'  # between duration and label (optional)
    sep_duration = b'\x14'  # after timestamp

    @cached_property
    def annotations(self):

        def strip_trash(event):
            return event.lstrip(b'\x00').rstrip(self.sep_timestamp)

        def is_true_event(event):
            return len(event.split(self.sep_timestamp)) > 1

        def parse_event(event):
            timestamp_str, event = event.split(self.sep_timestamp)
            timestamp = float(timestamp_str)
            optional = event.split(self.sep_duration)
            duration = None
            if len(optional) == 2:
                duration, label = optional
                duration = float(duration)
            else:
                label = optional[0]

            label = label.decode('ascii')
            return Annotation(timestamp, duration, label)

        events = self.signal[:].tobytes()
        events = events.split(self.sep_annotations)
        events = map(strip_trash, events)
        events = filter(is_true_event, events)
        events = map(parse_event, events)
        return list(events)
