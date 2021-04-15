__version__ = "0.4.0"
__all__ = ["Timeflake", "random", "from_values"]

import os
import time
from typing import Optional

from timeflake.flake import BASE62, HEX, Timeflake
from timeflake.utils import atoi


def parse(
    from_bytes: bytes = None, from_int=None, from_hex=None, from_base62=None
) -> Timeflake:
    b = None
    if from_bytes is not None:
        b = from_bytes
    elif from_base62 is not None:
        b = atoi(from_base62, BASE62).to_bytes(16, "big")
    elif from_hex is not None:
        b = atoi(from_hex.lower(), HEX).to_bytes(16, "big")
    elif from_int is not None:
        b = from_int.to_bytes(16, "big")
    else:
        raise ValueError("Must provide one of {bytes, int, hex, base62} ")
    return Timeflake(from_bytes=b)


def random() -> Timeflake:
    timestamp = int(time.time() * 1000)
    rand = int.from_bytes(os.urandom(10), "big", signed=False)
    value = ((timestamp << 80) | rand).to_bytes(16, "big")
    return Timeflake(from_bytes=value)


def from_values(timestamp: int, random: Optional[int] = None) -> Timeflake:
    if random is None:
        random = int.from_bytes(os.urandom(10), "big", signed=False)
    value = ((timestamp << 80) | random).to_bytes(16, "big")
    return Timeflake(from_bytes=value)
