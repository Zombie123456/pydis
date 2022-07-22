import threading

from .exceptions import NotFound, ExpiredError
from .value import Value


class SingletonType(type):
    _instance_lock = threading.Lock()
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Data(dict):
    def __getitem__(self, key: str):
        try:
            value: Value = super().__getitem__(key)
            if value.is_expired():
                self.pop(key)
                raise ExpiredError(key)
        except KeyError:
            raise NotFound(key)
        return value
