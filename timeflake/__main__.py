import argparse
from argparse import RawTextHelpFormatter

import timeflake


def main():
    DESCRIPTION = """Timeflake is a 128-bit, roughly-ordered, URL-safe UUID."""

    parser = argparse.ArgumentParser(
        description=DESCRIPTION, formatter_class=RawTextHelpFormatter
    )
    parser.add_argument(
        "-n",
        "--num",
        type=int,
        default=1,
        help="the number of flakes to generate (default: 1)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="include additional info for generated flakes",
    )

    args = parser.parse_args()

    for _ in range(args.num):
        flake = timeflake.random()
        if args.verbose:
            print(
                f"ts={flake.timestamp}\trand={flake.random}\tint={flake.int}\thex={flake.hex}\tbase62={flake.base62}"
            )
        else:
            print(flake)


if __name__ == "__main__":
    main()
