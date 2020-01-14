from timeflake.flake import DEFAULT_ALPHABET, DEFAULT_EPOCH, Timeflake

__all__ = ["Timeflake", "DEFAULT_ALPHABET", "DEFAULT_EPOCH", "random", "parse"]

_global_timeflake = Timeflake()
random = _global_timeflake.random
parse = _global_timeflake.parse
