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


class DatabaseMetaObject(CallbackCache):
    type: str
    guid: str


class SourceInfo(CallbackCache):
    promo_code: str
    refer: DatabaseMetaObject
    recorder: DatabaseMetaObject


class PriceItem(CallbackCache, prefix='tarch'):
    title: str
    tariff: DatabaseMetaObject
    price: QuantitativeInt
    discount: QuantitativeInt
    amount: QuantitativeInt
    source_info: SourceInfo | None = None


class PriceList(CallbackCache):
    self: DatabaseMetaObject
    price_items: list[PriceItem]


class Invoice(CallbackCache):
    self: DatabaseMetaObject
    subscription: DatabaseMetaObject
    counterparty: DatabaseMetaObject
    tariff: DatabaseMetaObject
    deadline: datetime
    price: QuantitativeInt
    discount: QuantitativeInt
    amount: QuantitativeInt


class SuccessfulPayment(CallbackCache):
    invoice: DatabaseMetaObject
    timestamp: datetime


class InvoiceStatus(CallbackCache):
    ok: bool
    error_message: str | None


class StartSubscriptionInfo(CallbackCache):
    next_payment_datetime: datetime
    period_text: str
    vpn_conf: str
