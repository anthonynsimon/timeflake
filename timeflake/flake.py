import math
import secrets
import time
from datetime import datetime

from timeflake.utils import atoi, itoa

# Default epoch for timestamp part
# 2020-01-01T00:00:00Z
DEFAULT_EPOCH = int(datetime(year=2020, month=1, day=1).strftime("%s"))
DEFAULT_ALPHABET = list("23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")
MAX_SEQUENCE_NUMBER = int(math.pow(2, 22)) - 1


class Timeflake:
    """
    Timeflakes are 64-bit roughly-ordered, globally-unique, URL-safe UUIDs.

    When using the random sequence number method, the probability of a collision per worker
    per second is 2^22 (about 1 in 4 million).

    When using the default epoch (2020-01-01), the IDs will run out at around 2088-01-19.

    :param shard_id: an int between 0 and 1023 representing the assigned logical shard id.
    :param encoding: valid values are 'uint64' and 'base57' (default).
    :param epoch: the custom epoch.
    :param timefunc: a time function which returns the current unix time in seconds as an
    int (optionally with millis as decimal points).
    """

    def __init__(
        self, shard_id=None, encoding="base57", epoch=DEFAULT_EPOCH, timefunc=time.time
    ):
        if shard_id is not None:
            assert isinstance(
                shard_id, int
            ), "shard_id must be an int (no decimal points)"
            assert 0 <= shard_id <= 1023, "shard_id must be between 0 and 1023"
            self._shard_id = shard_id
        else:
            self._shard_id = secrets.randbits(10)
        assert encoding in {"base57", "uint64"}
        self._epoch = epoch
        self._last_tick = 0
        self._sequence = -1
        self._encoding = encoding
        self._timefunc = timefunc

    @property
    def shard_id(self):
        return self._shard_id

    @property
    def epoch(self):
        return self._epoch

    def next(self):
        """
        Returns a new UUID using the next sequence number increment for the assigned shard ID.
        """
        timestamp = int(self._timefunc() - self._epoch)
        if timestamp > self._last_tick:
            self._last_tick = timestamp
            self._sequence = -1
        self._sequence = (self._sequence + 1) % MAX_SEQUENCE_NUMBER
        flake = (timestamp << 32) + (self._shard_id << 22) + self._sequence
        return self._encode(flake)

    def random(self):
        """
        Returns a new UUID using cryptographically strong pseudo-random numbers for the sequence number.
        """
        timestamp = int(self._timefunc() - self._epoch)
        flake = (timestamp << 32) + (self._shard_id << 22) + secrets.randbits(22)
        return self._encode(flake)

    def parse(self, flake):
        """
        Parses a flake and returns a tuple with the parts: (timestamp, shard_id, sequence_number).
        """
        flake = self._decode(flake)
        timestamp = self._epoch + self._extract_bits(flake, 32, 32)
        shard_id = self._extract_bits(flake, 22, 10)
        sequence_number = self._extract_bits(flake, 0, 22)
        return (timestamp, shard_id, sequence_number)

    @classmethod
    def _extract_bits(cls, data, shift, length):
        """
        Extract a portion of a bit string in it's integer form.
        """
        bitmask = ((1 << length) - 1) << shift
        return (data & bitmask) >> shift

    def _encode(self, value):
        if self._encoding == "base57":
            return itoa(value, DEFAULT_ALPHABET)
        elif self._encoding == "uint64":
            return value
        else:
            raise NotImplementedError(
                f"Encoding for type: '{self._encoding}' has not being implemented."
            )

    def _decode(self, value):
        if self._encoding == "base57":
            return atoi(value, DEFAULT_ALPHABET)
        elif self._encoding == "uint64":
            return value
        else:
            raise NotImplementedError(
                f"Encoding for type: '{self._encoding}' has not being implemented."
            )

