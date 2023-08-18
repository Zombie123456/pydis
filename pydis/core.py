import pickle
import threading
import time
from typing import Any, Optional, List

from .utils import SingletonType, Data
from .value import Value
from .exceptions import ExpiredError, NotFound, NoConfigKeyError


class Config(metaclass=SingletonType):
    # 全局的timeout，如果在设置key没有指定timeout的话，就会应用该timeout
    default_timeout: Optional[int] = None

    config_keys = ['default_timeout']

    @classmethod
    def set_config(cls, key, value):
        if key not in cls.config_keys:
            raise NoConfigKeyError(key)
        setattr(cls, key, value)


class Pydis(metaclass=SingletonType):
    _data: Data[str, Value] = Data()
    config = Config()

    def set_config(self, key, value):
        self.config.set_config(key, value)

    def force_clean(self) -> None:
        """
        删除所有的keys，没有过期的key也会被删除，慎用
        :return:
        """
        self._data.clear()

    def clean(self) -> None:
        """
        删除已经过期的key
        :return:
        """
        expired_keys = [key for key, value in self._data.items() if value.is_expired()]
        self.delete_many(expired_keys)

    def get(self, key: str) -> Any:
        try:
            value = self._data[key]
        except (NotFound, ExpiredError):
            return None
        return value.value

    def set_nx(self, key: str, value: Any, timeout: Optional[int] = None) -> bool:
        """
        没有key的时候设置key，返回True
        有key的时候不做任何操作，返回False
        """
        if self.get(key) is not None:
            return False
        self._set(key, value, timeout)
        return True

    def set(self, key: str, value: Any, timeout: Optional[int] = None) -> None:
        self._set(key, value, timeout)

    def _set(self, key: str, value: Any, timeout: Optional[int] = None) -> None:
        if timeout is None:
            timeout = self.config.default_timeout
        value = Value(value, timeout=timeout)
        self._data[key] = value

    def delete(self, key: str) -> None:
        try:
            del self._data[key]
        except (NotFound, ExpiredError):
            return None

    def ttl(self, key: str) -> int:
        """
        返回持续时间，如果key不存在返回-2，永久key返回-1，其他情况，返回具体的到期时间
        :param key:
        :return:
        """
        try:
            value = self._data[key]
        except (NotFound, ExpiredError):
            return -2
        return value.ttl()

    def _incr(self, key: str, amplitude: int, func: str) -> int:
        value = self._data[key]
        value.incr(amplitude, func)
        return value.value

    def incr(self, key: str, amplitude: int = 1) -> int:
        return self._incr(key, amplitude, 'incr')

    def decr(self, key: str, amplitude: int = 1) -> int:
        return self._incr(key, -amplitude, 'decr')

    def set_many(self, data: dict, timeout: Optional[int] = None) -> None:
        if timeout is None:
            timeout = self.config.default_timeout

        for key, value in data.items():
            data[key] = Value(value, timeout)
        self._data.update(data)

    def delete_many(self, keys: List[str]) -> None:
        _ = [self.delete(key) for key in keys]

    def size(self) -> int:
        return len(self._data)

    def keys(self) -> List:
        """
        以列表形式返回所有的key
        :return:
        """
        keys = []
        expired_keys = []
        for key, value in self._data.items():
            if value.is_expired():
                expired_keys.append(key)
            else:
                keys.append(key)

        self.delete_many(expired_keys)
        return keys

    def is_empty(self) -> bool:
        return bool(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def save(self, path: str) -> None:
        kv = {}
        for key in self.keys():
            try:
                kv[key] = self._data[key].value
            except (NotFound, ExpiredError):
                pass
        with open(path, 'wb') as f:
            pickle.dump(kv, f)

    def load(self, path: str, nx: bool = False) -> None:
        with open(path, 'rb') as f:
            obj = pickle.load(f)
            for key in obj.keys():
                if nx:
                    self.set_nx(key, obj[key])
                else:
                    self.set(key, obj[key])
