def itoa(num, alphabet):
    """
    Converts an int to a str, using the given alphabet.
    """
    value = ""
    size = len(alphabet)
    while num:
        num, index = divmod(num, size)
        value += alphabet[index]
    return value[::-1]


def atoi(value, alphabet):
    """
    Converts a str to an int, using the given alphabet.
    """
    num = 0
    size = len(alphabet)
    for char in value:
        num = num * size + alphabet.index(char)
    return num
