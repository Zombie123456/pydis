from typing import Any, Optional, List

from .utils import SingletonType, Data
from .value import Value
from .exceptions import ExpiredError, NotFound


class Pydis(metaclass=SingletonType):
    _data: Data[str, Value] = Data()

    def __init__(self, default_timeout: Optional[int] = None):
        """
        :param default_timeout: 全局的timeout，如果在设置key没有指定timeout的话，就会应用该timeout
        """
        self.default_timeout = default_timeout

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
        _ = [self.delete(expired_key) for expired_key in expired_keys]

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
            timeout = self.default_timeout
        value = Value(value, timeout=timeout)
        self._data[key] = value

    def delete(self, key: str) -> None:
        self._data.pop(key, None)

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

        _ = [self.delete(expired_key) for expired_key in expired_keys]
        return keys

    def is_empty(self) -> bool:
        return bool(self._data)

    def __len__(self):
        return len(self._data)
