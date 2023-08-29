import re

NUM_OR_DOT_REGEX = re.compile(r'^[0-9.]$')


def isNumOrDot(string: str):
    return bool(NUM_OR_DOT_REGEX.search(string))


def convertToNumber(string: str):

    number = (float(string) * -1)

    if number.is_integer():
        number = int(number)

    return number


def isEmpty(string: str):
    return len(string) == 0


def isValidNumber(string: str):
    valid = False
    try:
        float(string)
        valid = True
    except ValueError:
        valid = False
    return valid
