import timeit


def main():
    res = timeit.repeat("timeflake.random()", setup="import timeflake", number=int(1e5))
    print(f"timeflake.random: {res}")

    res = timeit.repeat("timeflake.next()", setup="import timeflake", number=int(1e5))
    print(f"timeflake.next: {res}")

    res = timeit.repeat("uuid.uuid4()", setup="import uuid", number=int(1e5))
    print(f"uuid.uuid4: {res}")


if __name__ == "__main__":
    main()
