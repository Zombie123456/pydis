from typing import Any, Optional, Tuple
from datetime import datetime, timedelta


class Value:
    def __init__(self, value: Any, timeout: Optional[float]):
        self.is_forever, self.expired_to = self.__load_expired_to(timeout)
        self.can_incr = isinstance(value, int)
        self.value = value

    @staticmethod
    def __load_expired_to(timeout: Optional[float]) -> Tuple[bool, Optional[datetime]]:
        if timeout is None:
            is_forever = True
            expired_to = None
        else:
            if timeout <= 0:
                raise ValueError("Make sure timeout is an float greater than 0 ")
            is_forever = False
            expired_to = datetime.now() + timedelta(seconds=timeout)
        return is_forever, expired_to

    def is_expired(self) -> bool:
        if self.is_forever:
            return False
        return self.expired_to < datetime.now()

    def ttl(self) -> int:
        if self.is_forever:
            return -1
        return (self.expired_to - datetime.now()).seconds

    def incr(self, amplitude: int, func: str) -> None:
        if not self.can_incr:
            raise ValueError(f"type: {type(self.value)} no support {func}")
        self.value += amplitude
