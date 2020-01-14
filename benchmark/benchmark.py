import timeit


def main():
    res = timeit.timeit(
        "timeflake.parse(flake)", setup="import timeflake; flake = timeflake.random()"
    )
    print(f"timeflake.parse: {res}")

    res = timeit.timeit("timeflake.random()", setup="import timeflake")
    print(f"timeflake.random: {res}")

    res = timeit.timeit(
        "flake.next()", setup="import timeflake; flake = timeflake.Timeflake()"
    )
    print(f"timeflake.next: {res}")

    res = timeit.timeit("uuid.uuid4()", setup="import uuid")
    print(f"uuid.uuid4: {res}")

    res = timeit.timeit("uuid.uuid1()", setup="import uuid")
    print(f"uuid.uuid1: {res}")


if __name__ == "__main__":
    main()
