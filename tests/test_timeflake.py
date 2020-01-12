import time
from timeflake import Timeflake
from timeflake.flake import MAX_COUNTER_VALUE


def test_shard_id():
    start_ts = int(time.time())
    timeflake = Timeflake(shard_id=123)
    flake = timeflake.next()
    timestamp, shard_id, counter = timeflake.parse(flake)
    assert isinstance(flake, str)
    assert 0 < len(flake) <= 11
    assert start_ts <= timestamp
    assert shard_id == 123
    assert counter == 0

    # Test increment changed UUID
    new_flake = timeflake.next()
    new_timestamp, new_shard_id, new_counter = timeflake.parse(new_flake)
    assert isinstance(new_flake, str)
    assert new_flake != flake
    assert 0 < len(new_flake) <= 11
    assert start_ts <= new_timestamp
    assert new_shard_id == 123
    assert new_counter == 1


def test_random():
    now = int(time.time())
    timeflake = Timeflake(timefunc=lambda: now)
    for i in range(1000):
        flake = timeflake.next()
        timestamp, shard_id, counter = timeflake.parse(flake)
        assert isinstance(flake, str)
        assert 0 < len(flake) <= 11
        assert now == timestamp
        assert 0 <= shard_id <= 1023
        assert counter == i


def test_counter_restart():
    now = int(time.time())
    timeflake = Timeflake(shard_id=123, timefunc=lambda: now)
    # Let's speed up the test
    timeflake.next()  # discard first value (it will take the timestamp here)
    initial_counter = MAX_COUNTER_VALUE - 100
    timeflake._counter = initial_counter

    # Ensure counter restarts when exceeds limit per shard_id and timestamp second
    for i in range(initial_counter, MAX_COUNTER_VALUE - 1):
        flake = timeflake.next()
        timestamp, shard_id, counter = timeflake.parse(flake)
        assert isinstance(flake, str)
        assert 0 < len(flake) <= 11
        assert now == timestamp
        assert shard_id == 123
        assert counter == i + 1

    # Check that the counter restarts
    for i in range(100):
        flake = timeflake.next()
        timestamp, shard_id, counter = timeflake.parse(flake)
        assert isinstance(flake, str)
        assert 0 < len(flake) <= 11
        assert now == timestamp
        assert shard_id == 123
        assert counter == i


def test_uint64():
    now = int(time.time())
    timeflake = Timeflake(encoding="uint64", timefunc=lambda: now)
    for i in range(1000):
        flake = timeflake.random()
        timestamp, shard_id, counter = timeflake.parse(flake)
        assert isinstance(flake, int)
        assert now == timestamp
        assert 0 <= shard_id <= 1023
        assert counter != i


def test_timestamp():
    now = int(time.time())
    timeflake = Timeflake()

    flake1 = timeflake.next()
    timestamp1, shard_id1, counter1 = timeflake.parse(flake1)
    assert isinstance(flake1, str)
    assert now == timestamp1
    assert counter1 == 0

    flake2 = timeflake.next()
    timestamp2, shard_id2, counter2 = timeflake.parse(flake2)
    assert isinstance(flake2, str)
    assert now == timestamp2
    assert shard_id2 == shard_id1
    assert counter2 == 1

    # Wait
    time.sleep(1)

    flake3 = timeflake.next()
    timestamp3, shard_id3, counter3 = timeflake.parse(flake3)
    assert isinstance(flake3, str)
    assert flake1 != flake3
    assert flake2 != flake3
    assert timestamp1 < timestamp3
    assert now == timestamp3 - 1
    assert shard_id1 == shard_id2
    assert counter1 == counter3

