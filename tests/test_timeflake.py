import time
import uuid

import timeflake
import timeflake.flake


def test_random():
    now = int(time.time())
    for i in range(1000):
        flake = timeflake.random()
        assert isinstance(flake, timeflake.Timeflake)
        rand = flake.random
        timestamp = flake.timestamp
        assert isinstance(rand, int)
        assert isinstance(timestamp, int)
        assert 0 <= flake.int <= timeflake.flake.MAX_TIMEFLAKE
        assert now <= timestamp
        assert 0 <= rand <= timeflake.flake.MAX_RANDOM
        assert 0 <= timestamp <= timeflake.flake.MAX_TIMESTAMP


def test_from_values_timestamp_only():
    now = 123
    for i in range(1000):
        flake = timeflake.from_values(timestamp=now)
        assert isinstance(flake, timeflake.Timeflake)
        assert isinstance(flake.random, int)
        assert isinstance(flake.timestamp, int)
        assert 0 <= flake.int <= timeflake.flake.MAX_TIMEFLAKE
        assert 0 <= flake.random <= timeflake.flake.MAX_RANDOM
        assert now == flake.timestamp


def test_from_values_timestamp_and_random():
    now = 123
    rand = 456
    for i in range(1000):
        flake = timeflake.from_values(timestamp=now, random=rand)
        assert isinstance(flake, timeflake.Timeflake)
        assert isinstance(flake.random, int)
        assert isinstance(flake.timestamp, int)
        assert 0 <= flake.int <= timeflake.flake.MAX_TIMEFLAKE
        assert now == flake.timestamp
        assert rand == flake.random


def test_parse_base62_and_conversions():
    flake = timeflake.parse(from_base62="02i1KoFfY3auBS745gImbZ")
    assert isinstance(flake, timeflake.Timeflake)
    assert isinstance(flake.random, int)
    assert isinstance(flake.timestamp, int)
    assert flake.timestamp == 1579091935216
    assert flake.random == 724773312193627487660233
    assert flake.int == 1909005012028578488143182045514754249
    assert flake.hex == "016fa936bff0997a0a3c428548fee8c9"
    assert flake.base62 == "02i1KoFfY3auBS745gImbZ"
    assert flake.bytes == b"\x01o\xa96\xbf\xf0\x99z\n<B\x85H\xfe\xe8\xc9"
    assert flake.uuid == uuid.UUID("016fa936-bff0-997a-0a3c-428548fee8c9")


def test_parse_bytes_and_conversions():
    flake = timeflake.parse(from_bytes=b"\x01o\xa96\xbf\xf0\x99z\n<B\x85H\xfe\xe8\xc9")
    assert isinstance(flake, timeflake.Timeflake)
    assert isinstance(flake.random, int)
    assert isinstance(flake.timestamp, int)
    assert flake.timestamp == 1579091935216
    assert flake.random == 724773312193627487660233
    assert flake.int == 1909005012028578488143182045514754249
    assert flake.hex == "016fa936bff0997a0a3c428548fee8c9"
    assert flake.base62 == "02i1KoFfY3auBS745gImbZ"
    assert flake.bytes == b"\x01o\xa96\xbf\xf0\x99z\n<B\x85H\xfe\xe8\xc9"
    assert flake.uuid == uuid.UUID("016fa936-bff0-997a-0a3c-428548fee8c9")


def test_parse_hex_and_conversions():
    flake = timeflake.parse(from_hex="016fa936bff0997a0a3c428548fee8c9")
    assert isinstance(flake, timeflake.Timeflake)
    assert isinstance(flake.random, int)
    assert isinstance(flake.timestamp, int)
    assert flake.timestamp == 1579091935216
    assert flake.random == 724773312193627487660233
    assert flake.int == 1909005012028578488143182045514754249
    assert flake.hex == "016fa936bff0997a0a3c428548fee8c9"
    assert flake.base62 == "02i1KoFfY3auBS745gImbZ"
    assert flake.bytes == b"\x01o\xa96\xbf\xf0\x99z\n<B\x85H\xfe\xe8\xc9"
    assert flake.uuid == uuid.UUID("016fa936-bff0-997a-0a3c-428548fee8c9")


def test_parse_int_and_conversions():
    flake = timeflake.parse(from_int=1909005012028578488143182045514754249)
    assert isinstance(flake, timeflake.Timeflake)
    assert isinstance(flake.random, int)
    assert isinstance(flake.timestamp, int)
    assert flake.timestamp == 1579091935216
    assert flake.random == 724773312193627487660233
    assert flake.int == 1909005012028578488143182045514754249
    assert flake.hex == "016fa936bff0997a0a3c428548fee8c9"
    assert flake.base62 == "02i1KoFfY3auBS745gImbZ"
    assert flake.bytes == b"\x01o\xa96\xbf\xf0\x99z\n<B\x85H\xfe\xe8\xc9"
    assert flake.uuid == uuid.UUID("016fa936-bff0-997a-0a3c-428548fee8c9")


def test_timestamp_increment():
    flake1 = timeflake.random()
    time.sleep(0.4)
    flake2 = timeflake.random()
    time.sleep(1.1)
    flake3 = timeflake.random()

    assert flake1 < flake2 < flake3
    assert flake1.timestamp < flake2.timestamp < flake3.timestamp
    assert len(set([flake1.timestamp, flake2.timestamp, flake3.timestamp])) == 3


def test_uniqueness():
    seen = set()
    for i in range(int(1e6)):
        flake = timeflake.random()
        key = flake.base62
        if key in seen:
            raise Exception(f"Flake collision found after {i} generations")
        assert len(key) == 22
        seen.add(flake.base62)
