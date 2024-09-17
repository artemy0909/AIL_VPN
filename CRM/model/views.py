from _decimal import Decimal

from utils.callback_stored import CallbackCache


class QuantitativeInt(CallbackCache):
    value: int
    currency_symbol: str
    semicolons: int = 2

    def __post__init__(self, value: float, unit_symbol: str, semicolons: int = 2):
        self.value: int = int(Decimal(str(value)) * (10 ** semicolons))
        self.currency_symbol: str = unit_symbol
        self.semicolons: int = semicolons

    def __str__(self):
        integral_part = self.value // (10 ** self.semicolons)
        fractional_part = self.value % (10 ** self.semicolons)

        fractional_str = f"{fractional_part:0{self.semicolons}d}"

        return f"{integral_part}.{fractional_str} {self.currency_symbol}"

    def __int__(self):
        return self.value


class PromoCode(CallbackCache):
    promo_code: str
    refer_guid: str
    source_guid: str


class PriceItem(CallbackCache, prefix='tarch'):
    title: str
    tariff_guid: str
    price: QuantitativeInt
    discount: QuantitativeInt
    amount: QuantitativeInt
    promo_code: PromoCode | None = None


class PriceList(CallbackCache):
    price_items: list[PriceItem]
