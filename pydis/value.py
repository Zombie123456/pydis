from typing import Any, Optional, Tuple
from datetime import datetime, timedelta


class Value:
    def __init__(self, value: Any, timeout: Optional[float]):
        self.value = value
        self.forever_key, self.expired_to = self.__load_expired_to(timeout)
        self.can_incr = isinstance(value, int)

    @staticmethod
    def __load_expired_to(timeout: Optional[float]) -> Tuple[bool, Optional[datetime]]:
        if timeout is None:
            forever = True
            expired_to = None
        else:
            if timeout <= 0:
                raise ValueError("Make sure timeout is an integer greater than 0 ")
            forever = False
            expired_to = datetime.now() + timedelta(seconds=timeout)
        return forever, expired_to

    def is_expired(self) -> bool:
        """
        是否超时
        :return:
            Ture : 超时
            False: 没超时
        """
        if self.forever_key:
            return False
        return self.expired_to < datetime.now()

    def ttl(self) -> int:
        if self.forever_key:
            return -1
        return (self.expired_to - datetime.now()).seconds

    def _incr(self, amplitude: int, func: str) -> None:
        if not self.can_incr:
            raise ValueError(f"type: {type(self.value)} no support {func}")
        self.value += amplitude

    def incr(self, amplitude: int) -> None:
        self._incr(amplitude, 'incr')

    def decr(self, amplitude: int) -> None:
        self._incr(-amplitude, 'decr')
