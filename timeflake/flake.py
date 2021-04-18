import time
import uuid
from functools import lru_cache

from timeflake.utils import atoi, itoa

BASE62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
HEX = "0123456789abcdef"
MAX_TIMESTAMP = 281474976710655
MAX_RANDOM = 1208925819614629174706175
MAX_TIMEFLAKE = 340282366920938463463374607431768211455


class Timeflake(uuid.UUID):
    def __init__(self, from_bytes: bytes):
        if from_bytes is None:
            raise ValueError("from_bytes is a required parameter")
        super(self.__class__, self).__init__(bytes=from_bytes)
        # Validate flake
        as_int = self.int
        if as_int < 0 or MAX_TIMEFLAKE < as_int:
            raise ValueError("Invalid flake provided")

    @property
    def uuid(self) -> uuid.UUID:
        return uuid.UUID(bytes=self.bytes)

    @property
    @lru_cache(1)
    def base62(self) -> str:
        return itoa(self.int, BASE62, padding=22)

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
        return f"Timeflake('{self.hex}')"

    def __str__(self) -> str:
        return self.base62
