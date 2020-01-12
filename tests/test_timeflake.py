import time
from timeflake import Timeflake
from timeflake.flake import MAX_SEQUENCE_NUMBER


def test_shard_id():
    start_ts = int(time.time())
    timeflake = Timeflake(shard_id=123)
    flake = timeflake.next()
    timestamp, shard_id, sequence = timeflake.parse(flake)
    assert isinstance(flake, str)
    assert 0 < len(flake) <= 11
    assert start_ts <= timestamp
    assert shard_id == 123
    assert sequence == 0

    # Test increment changed UUID
    new_flake = timeflake.next()
    new_timestamp, new_shard_id, new_sequence = timeflake.parse(new_flake)
    assert isinstance(new_flake, str)
    assert new_flake != flake
    assert 0 < len(new_flake) <= 11
    assert start_ts <= new_timestamp
    assert new_shard_id == 123
    assert new_sequence == 1


def test_random():
    now = int(time.time())
    timeflake = Timeflake(timefunc=lambda: now)
    for i in range(1000):
        flake = timeflake.next()
        timestamp, shard_id, sequence = timeflake.parse(flake)
        assert isinstance(flake, str)
        assert 0 < len(flake) <= 11
        assert now == timestamp
        assert 0 <= shard_id <= 1023
        assert sequence == i


def test_sequence_restart():
    now = int(time.time())
    timeflake = Timeflake(shard_id=123, timefunc=lambda: now)
    # Let's speed up the test
    timeflake.next()  # discard first value (it will take the timestamp here)
    initial_sequence = MAX_SEQUENCE_NUMBER - 100
    timeflake._sequence = initial_sequence

    # Ensure sequence restarts when exceeds limit per shard_id and timestamp second
    for i in range(initial_sequence, MAX_SEQUENCE_NUMBER - 1):
        flake = timeflake.next()
        timestamp, shard_id, sequence = timeflake.parse(flake)
        assert isinstance(flake, str)
        assert 0 < len(flake) <= 11
        assert now == timestamp
        assert shard_id == 123
        assert sequence == i + 1

    # Check that the sequence restarts
    for i in range(100):
        flake = timeflake.next()
        timestamp, shard_id, sequence = timeflake.parse(flake)
        assert isinstance(flake, str)
        assert 0 < len(flake) <= 11
        assert now == timestamp
        assert shard_id == 123
        assert sequence == i


def test_uint64():
    now = int(time.time())
    timeflake = Timeflake(encoding="uint64", timefunc=lambda: now)
    for i in range(1000):
        flake = timeflake.random()
        timestamp, shard_id, sequence = timeflake.parse(flake)
        assert isinstance(flake, int)
        assert now == timestamp
        assert 0 <= shard_id <= 1023
        assert sequence != i


def test_timestamp():
    now = int(time.time())
    timeflake = Timeflake()

    flake1 = timeflake.next()
    timestamp1, shard_id1, sequence1 = timeflake.parse(flake1)
    assert isinstance(flake1, str)
    assert now == timestamp1
    assert sequence1 == 0

    flake2 = timeflake.next()
    timestamp2, shard_id2, sequence2 = timeflake.parse(flake2)
    assert isinstance(flake2, str)
    assert now == timestamp2
    assert shard_id2 == shard_id1
    assert sequence2 == 1

    # Wait
    time.sleep(1)

    flake3 = timeflake.next()
    timestamp3, shard_id3, sequence3 = timeflake.parse(flake3)
    assert isinstance(flake3, str)
    assert flake1 != flake3
    assert flake2 != flake3
    assert timestamp1 < timestamp3
    assert now == timestamp3 - 1
    assert shard_id1 == shard_id2
    assert sequence1 == sequence3

