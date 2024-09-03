from aiogram.filters.callback_data import CallbackData


class PriceChoiceCallback(CallbackData, prefix='prch'):
    article: str
