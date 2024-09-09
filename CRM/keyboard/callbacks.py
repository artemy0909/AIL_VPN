from aiogram.filters.callback_data import CallbackData


class TariffChoiceCallback(CallbackData, prefix='tarch'):
    tariff_guid: str
    amount: int

    data_key: int
