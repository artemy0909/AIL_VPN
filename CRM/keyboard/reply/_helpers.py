from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def reply_keyboard(func):
    def wrapper(*args, **kwargs) -> ReplyKeyboardMarkup:

        def error():
            raise TypeError(f"Expected str | list[str] | tuple[str]")

        res: list[str] = func(*args, **kwargs)

        if isinstance(res, str):
            return ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=res)]],
                resize_keyboard=True,
                one_time_keyboard=False
            )
        elif isinstance(res, (list, tuple)):
            for e in res:
                if not isinstance(e, str):
                    error()
            buttons = [[KeyboardButton(text=e)] for e in res]
            return ReplyKeyboardMarkup(
                keyboard=buttons,
                resize_keyboard=True,
                one_time_keyboard=False
            )
        else:
            error()

    return wrapper
