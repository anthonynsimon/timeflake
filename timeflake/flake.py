import time
import uuid
from functools import lru_cache

from timeflake.utils import atoi, itoa

BASE54 = "0123456789ABCDEFGHJKMNPQRSTVWXYZabcdefghjkmnpqrstvwxyz"
HEX = "0123456789abcdef"
MAX_TIMESTAMP = 281474976710655
MAX_RANDOM = 1208925819614629174706175
MAX_TIMEFLAKE = 340282366920938463463374607431768211455


class Timeflake:
    def __init__(self, from_bytes: bytes):
        if from_bytes is None:
            raise ValueError("from_bytes is a required parameter")
        self._bytes = from_bytes
        # Validate flake
        as_int = self.int
        if as_int < 0 or MAX_TIMEFLAKE < as_int:
            raise ValueError("Invalid flake provided")

    @property
    def bytes(self) -> bytes:
        return self._bytes

    @property
    def uuid(self) -> uuid.UUID:
        return uuid.UUID(bytes=self.bytes)

    @property
    def int(self) -> int:
        return int.from_bytes(self.bytes, "big", signed=False)

    @property
    @lru_cache(1)
    def hex(self) -> str:
        return itoa(self.int, HEX, padding=32)

    @property
    @lru_cache(1)
    def base54(self) -> str:
        return itoa(self.int, BASE54, padding=23)

    @property
    def timestamp(self) -> int:
        return self.int >> 80

    @property
    def random(self) -> int:
        return self.int & MAX_RANDOM

    def __hash__(self) -> int:
        return self.int

    def __eq__(self, other) -> bool:
        if not isinstance(other, Timeflake):
            return False
        return other.int == self.int

    def __lt__(self, other) -> bool:
        return self.int < other.int

    def __repr__(self) -> str:
        return f"Timeflake(base54='{self.base54}')"

    def __str__(self) -> str:
        return self.base54
