from utils.callback_stored import CallbackDataStored


class TariffChoiceCallback(CallbackDataStored, prefix='tarch'):
    tariff_guid: str
    amount: int
    promo_code: str = None
    reffer_guid: str = None # todo переименовать

