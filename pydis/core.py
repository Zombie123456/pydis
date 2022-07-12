from typing import Dict, Any, Optional, List

from .utils import SingletonType
from .value import Value


class Pydis(metaclass=SingletonType):
    _data: Dict[str, Value] = {}

    def __init__(self, default_timeout: Optional[int] = None):
        """
        :param default_timeout: 全局的timeout，如果在设置key没有指定timeout的话，就会应用该timeout
        """
        self.default_timeout = default_timeout

    def get(self, key: str) -> Any:
        try:
            value = self._data[key]
        except KeyError:
            return None

        if value.is_expired():
            self.delete(key)
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
        except KeyError:
            return -2
        if value.is_expired():
            self.delete(key)
            return -2
        return value.ttl()

    def _incr(self, key: str, amplitude: int, func: str) -> int:
        try:
            value = self._data[key]
        except KeyError:
            raise KeyError(f'key: {key} does not exists')
        value.incr(amplitude, func)
        return value.value

    def incr(self, key: str, amplitude: int = 1) -> int:
        self._incr(key, amplitude, 'incr')

    def decr(self, key: str, amplitude: int = 1) -> int:
        return self._incr(key, -amplitude, 'decr')

    def keys(self) -> List:
        keys_dict: List = []
        for key, value in self._data.items():
            if value.is_expired():
                self.delete(key)
                continue
            keys_dict.append(key)
        return keys_dict
