try:
    from functools import cached_property
except ImportError:
    from cached_property import cached_property  # type: ignore

__all__ = ['cached_property']
