import threading


class SingletonType(type):
    _instance_lock = threading.Lock()
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super().__call__(*args, **kwargs)
        return cls._instance
