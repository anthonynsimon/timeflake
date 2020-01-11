import collections
import secrets
import time
from datetime import datetime

from timeflake.utils import atoi, itoa

# Default epoch for timestamp part
# 2020-01-01T00:00:00Z
DEFAULT_EPOCH = int(datetime(year=2020, month=1, day=1).strftime("%s"))
DEFAULT_ALPHABET = list("23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")


class Timeflake:
    """
    A 64-bit (unsigned), roughly-ordered, globally-unique ID.

    When using random counter, the probability of a collision per second per worker is 2^22 (about 1 in 4 million).

    When using the default epoch (2020-01-01), the IDs will run out at around 2088-01-19.
    """

    def __init__(self, shard_id=None, encoded=True, epoch=DEFAULT_EPOCH):
        if shard_id is not None:
            assert isinstance(
                shard_id, int
            ), "shard_id must be an int (no decimal points)"
            assert 0 <= shard_id <= 1023, "shard_id must be between 0 and 1023"
            self._shard_id = shard_id
        else:
            self._shard_id = secrets.randbits(10)
        self._epoch = epoch
        self._last_tick = 0
        self._counter = -1
        self._encoded = encoded

    @property
    def shard_id(self):
        return self._shard_id

    @property
    def epoch(self):
        return self._epoch

    def next(self):
        timestamp = int(time.time() - self._epoch)
        if timestamp > self._last_tick:
            self._last_tick = timestamp
            self._counter = -1
        self._counter += 1
        timeflake = (timestamp << 32) + (self._shard_id << 22) + self._counter
        if self._encoded:
            return itoa(timeflake, DEFAULT_ALPHABET)
        return timeflake

    def random(self):
        timestamp = int(time.time() - self._epoch)
        timeflake = (timestamp << 32) + (self._shard_id << 22) + secrets.randbits(22)
        if self._encoded:
            return itoa(timeflake, DEFAULT_ALPHABET)
        return timeflake

    def parse(self, timeflake):
        """
        Parses a timeflake and returns a tuple with the parts: (timestamp, shard_id, counter).
        """
        if self._encoded:
            timeflake = atoi(timeflake, DEFAULT_ALPHABET)
        timestamp = self._epoch + self._extract_bits(timeflake, 32, 32)
        shard_id = self._extract_bits(timeflake, 22, 10)
        counter = self._extract_bits(timeflake, 0, 22)
        return (timestamp, shard_id, counter)

    @classmethod
    def _extract_bits(cls, data, shift, length):
        """
        Extract a portion of a bit string in it's integer form.
        """
        bitmask = ((1 << length) - 1) << shift
        return (data & bitmask) >> shift
