from random import choice
from string import ascii_letters, digits


def generate_token(length: int):
    return ''.join(choice(ascii_letters + digits) for _ in range(length))


def benchmark(func):
    from datetime import datetime

    def wrapper(*args, **kwargs):
        t = datetime.now()
        res = func(*args, **kwargs)
        print(func.__name__, datetime.now() - t)
        return res

    return wrapper
