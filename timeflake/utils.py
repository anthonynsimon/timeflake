from functools import lru_cache


@lru_cache(2)
def _index_alphabet(alphabet):
    return {char: i for i, char in enumerate(alphabet)}


def itoa(value, alphabet, padding=None):
    """
    Converts an int value to a str, using the given alphabet.
    Padding can be computed as: ceil(log of max_val base alphabet_len)
    """
    if value < 0:
        raise ValueError("Only positive numbers are allowed")
    elif value == 0:
        return alphabet[0]

    result = ""
    base = len(alphabet)

    while value:
        value, rem = divmod(value, base)
        result = alphabet[rem] + result

    if padding:
        fill = max(padding - len(result), 0)
        result = (alphabet[0] * fill) + result

    return result


def atoi(value, alphabet):
    """
    Converts a str value to an int, using the given alphabet.
    """
    if value == alphabet[0]:
        return 0

    index = _index_alphabet(alphabet)
    result = 0
    base = len(alphabet)

    for char in value:
        result = result * base + index[char]

    return result
