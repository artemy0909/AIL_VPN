from utils.callback_stored import CallbackDataStored
from pydantic import BaseModel


class PromoCodeInfoItem(BaseModel):
    promo_code: str
    refer_guid: str
    source_guid: str


class TariffChoiceCallback(CallbackDataStored, prefix='tarch'):
    tariff_guid: str
    price: int
    discount: int
    amount: int
    promo_code_info: PromoCodeInfoItem | None = None
