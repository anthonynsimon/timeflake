import timeit


def main():
    res = timeit.timeit(
        "timeflake.parse(from_base54=value)",
        setup="import timeflake; value = timeflake.random().base54",
    )
    print(f"timeflake.parse(from_base54): {res}")

    res = timeit.timeit(
        "timeflake.parse(from_bytes=value)",
        setup="import timeflake; value = timeflake.random().bytes",
    )
    print(f"timeflake.parse(from_bytes): {res}")

    res = timeit.timeit(
        "timeflake.parse(from_hex=value)",
        setup="import timeflake; value = timeflake.random().hex",
    )
    print(f"timeflake.parse(from_hex): {res}")

    res = timeit.timeit(
        "timeflake.parse(from_int=value)",
        setup="import timeflake; value = timeflake.random().int",
    )
    print(f"timeflake.parse(from_int): {res}")

    res = timeit.timeit("timeflake.random()", setup="import timeflake")
    print(f"timeflake.random: {res}")

    res = timeit.timeit("uuid.uuid4()", setup="import uuid")
    print(f"uuid.uuid4: {res}")

    res = timeit.timeit("uuid.uuid1()", setup="import uuid")
    print(f"uuid.uuid1: {res}")


if __name__ == "__main__":
    main()
