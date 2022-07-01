from datetime import datetime, timedelta
from typing import Dict, Tuple, Any, Optional, Union, Iterable

from .utils import SingletonType


class Pydis(SingletonType):
    _data: Dict[str, Tuple[datetime, Any]] = {}

    def __init__(self, default_timeout: Optional[int] = None):
        """
        :param default_timeout: 全局的timeout，如果在设置key没有指定timeout的话，就会应用该timeout
        """
        self.default_timeout = default_timeout

    @staticmethod
    def _expired(expired_date: Union[None, datetime], now: datetime) -> bool:
        return now > expired_date

    def get(self, key: str) -> Any:
        try:
            expired_date, value = self._data[key]
        except KeyError:
            return None

        if self._is_forever_key(expired_date):
            return value

        if self._expired(expired_date, datetime.now()):
            self._data.pop(key, None)
            return None
        return value

    def set(self, key: str, value: Any, timeout: Optional[int] = None) -> None:
        if timeout is None:
            if self.default_timeout is None:
                expired_date = None
            else:
                expired_date = datetime.now() + timedelta(seconds=self.default_timeout)
        else:
            if timeout <= 0:
                raise ValueError("Make sure timeout is an integer greater than 0 ")
            expired_date = datetime.now() + timedelta(seconds=timeout)
        self._set(key, (expired_date, value))

    def _set(self, key: str, tuple_data: Tuple) -> None:
        self._data[key] = tuple_data

    @staticmethod
    def _is_forever_key(expired_date: Union[datetime | None]) -> bool:
        return expired_date is None

    def ttl(self, key: str) -> int:
        try:
            expired_date, _ = self._data[key]
        except KeyError:
            return -2

        if self._is_forever_key(expired_date):
            return -1

        now = datetime.now()
        if self._expired(expired_date, now):
            self._data.pop(key, None)
            return -2
        return (expired_date - now).seconds

    def incr(self, key: str) -> int:
        try:
            expired_date, value = self._data[key]
        except KeyError:
            raise KeyError(f'key: {key} does not exists')
        if not isinstance(value, int):
            raise ValueError('only int type support incr action')
        value += 1
        self._set(key, (expired_date, int(value)))
        return value

    def decr(self, key: str) -> int:
        try:
            expired_date, value = self._data[key]
        except KeyError:
            raise KeyError(f'key: {key} does not exists')

        if not isinstance(value, int):
            raise ValueError('only int type support decr action')
        value -= 1
        self._set(key, (expired_date, value))
        return value

    def keys(self) -> Iterable:
        now = datetime.now()
        for key, value in self._data.items():
            expired_date, _ = value
            if self._is_forever_key(expired_date):
                yield key
            elif not self._expired(expired_date, now):
                yield key
