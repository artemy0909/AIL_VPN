from text.static.start import HELLO_TEXT


def hello_customer(*, name: str):
    return f"<b>{name}, добро пожаловать!</b>\n\n" + HELLO_TEXT
