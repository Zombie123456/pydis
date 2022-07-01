import threading


class SingletonType:
    _instance_lock = threading.Lock()
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super(SingletonType, cls).__new__(cls, *args, **kwargs)
        return cls._instance
