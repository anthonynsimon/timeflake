import math
import os
import time

from timeflake.utils import atoi, itoa

# Default epoch for timestamp part
# 2020-01-01T00:00:00Z
DEFAULT_EPOCH = 1577836800
DEFAULT_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
MAX_SEQUENCE_NUMBER = 4194303

TIMESTAMP_MASK = ((1 << 32) - 1) << 32
SHARD_MASK = ((1 << 10) - 1) << 22
SEQUENCE_MASK = (1 << 22) - 1


class Timeflake:
    """
    Timeflakes are 64-bit roughly-ordered, globally-unique, URL-safe UUIDs.
    
    When using the random method, you should expect a collision to occur if you're creating
    IDs at a rate of 77,162 within a single second.
    
    Once that is not enough, you can transition to using the '.next()' method (shard + counter instead of random),
    giving you 4,194,304 IDs per shard per second.
    
    Please be aware that system clocks can go backwards, and leap seconds can change these probabilities.
    
    When using the default epoch (2020-01-01), the IDs will run out at around 2156-02-07T07:28:15Z,
    giving you 100+ years of IDs.
    
    Params:
    :param shard_id: an int between 0 and 1023 representing the assigned logical shard id
    (or random if not provided).
    :param encoding: valid values are 'uint64' and 'base62' (default).
    :param epoch: the custom epoch.
    :param timefunc: a time function which returns the current unix time in seconds as an
    int (optionally with millis as decimal points).
    """

    def __init__(
        self, shard_id=None, encoding="base62", epoch=DEFAULT_EPOCH, timefunc=time.time
    ):
        if shard_id is None:
            self._shard_id = int.from_bytes(os.urandom(2), "big", signed=False) >> 6
        else:
            if not isinstance(shard_id, int):
                raise ValueError("shard_id must be an int (no decimal points)")
            if not (0 <= shard_id <= 1023):
                raise ValueError("shard_id must be between 0 and 1023")
            self._shard_id = shard_id

        if encoding not in {"base62", "uint64"}:
            raise ValueError("Encoding must be one of 'base62' or 'uint64'")

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
        seq = (self._sequence + 1) % MAX_SEQUENCE_NUMBER
        flake = timestamp << 32 | self._shard_id << 22 | seq
        self._sequence = seq
        return self._encode(flake)

    def random(self):
        """
        Returns a new UUID using cryptographically strong pseudo-random numbers for the sequence number.
        """
        timestamp = int(self._timefunc() - self._epoch)
        random = int.from_bytes(os.urandom(4), "big", signed=False)
        flake = (timestamp << 32) | random
        return self._encode(flake)

    def parse(self, flake):
        """
        Parses a flake and returns a tuple with the parts: (timestamp, shard_id, sequence_number).
        """
        flake = self._decode(flake)
        timestamp = self._epoch + ((flake & TIMESTAMP_MASK) >> 32)
        shard_id = (flake & SHARD_MASK) >> 22
        sequence_number = flake & SEQUENCE_MASK
        return (timestamp, shard_id, sequence_number)

    def _encode(self, value):
        if self._encoding == "base62":
            return itoa(value, DEFAULT_ALPHABET)
        elif self._encoding == "uint64":
            return value

    def _decode(self, value):
        if self._encoding == "base62":
            return atoi(value, DEFAULT_ALPHABET)
        elif self._encoding == "uint64":
            return value
