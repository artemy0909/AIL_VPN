from _decimal import Decimal
from datetime import datetime

from utils.callback_stored import CallbackCache


class QuantitativeInt(CallbackCache):
    value: int
    unit_symbol: str
    semicolons: int = 2
    currency: str

    def __str__(self):
        integral_part = self.value // (10 ** self.semicolons)
        fractional_part = self.value % (10 ** self.semicolons)

        fractional_str = f"{fractional_part:0{self.semicolons}d}"

        return f"{integral_part}.{fractional_str} {self.unit_symbol}"

    def __int__(self):
        return self.value


class Recorder(CallbackCache):
    type: str
    guid: str


class SourceInfo(CallbackCache):
    promo_code: str
    refer_guid: str
    recorder: Recorder


class PriceItem(CallbackCache, prefix='tarch'):
    title: str
    tariff_guid: str
    price: QuantitativeInt
    discount: QuantitativeInt
    amount: QuantitativeInt
    source_info: SourceInfo | None = None


class PriceList(CallbackCache):
    price_items: list[PriceItem]


class Invoice(CallbackCache):
    guid: str
    tariff_guid: str
    deadline: datetime
    price: QuantitativeInt
    discount: QuantitativeInt
    amount: QuantitativeInt
