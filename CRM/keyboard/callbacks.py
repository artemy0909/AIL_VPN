from aiogram.filters.callback_data import CallbackData


class PriceChoiceCallback(CallbackData, prefix='prch'):
    tariff_guid: str
    amount: int
