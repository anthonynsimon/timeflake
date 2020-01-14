from functools import lru_cache
from typing import Dict


@lru_cache(1)
def _inverted_index_alphabet(alphabet) -> Dict[str, int]:
    return {ch: i for i, ch in enumerate(alphabet)}


@lru_cache(1)
def _index_alphabet(alphabet) -> Dict[int, str]:
    return {i: ch for i, ch in enumerate(alphabet)}


def itoa(num: int, alphabet: str) -> str:
    """
    Converts an int to a str, using the given alphabet.
    """
    index = _index_alphabet(alphabet)
    value = ""
    base = len(alphabet)
    while num:
        num, rem = divmod(num, base)
        value = index[rem] + value
    return value


def atoi(value: str, alphabet: str) -> int:
    """
    Converts a str to an int, using the given alphabet.
    """
    index = _inverted_index_alphabet(alphabet)
    num = 0
    base = len(alphabet)
    for char in value:
        num = num * base + index[char]
    return num
