import base64
import binascii
from random import choice
from string import ascii_letters, digits

from pydantic import ValidationError
from pydantic import BaseModel


def try_decode_base64(encoded: str, model_class: type[BaseModel]) -> BaseModel | str:
    try:
        return decode_base64(encoded, model_class)
    except (binascii.Error, ValidationError) as e:
        return encoded


def encode_base64(model: BaseModel) -> str:
    json_data = model.model_dump_json()
    return base64.urlsafe_b64encode(json_data.encode()).decode().rstrip("=")


def decode_base64(encoded: str, model_class: type[BaseModel]) -> BaseModel:
    padding = "=" * (-len(encoded) % 4)
    decoded_json = base64.urlsafe_b64decode(encoded + padding).decode()
    return model_class.model_validate_json(decoded_json)


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
