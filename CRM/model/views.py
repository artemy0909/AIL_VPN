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


class PriceItem(CallbackCache, prefix='prit'):
    title: str
    tariff: DatabaseMetaObject
    price: QuantitativeInt
    discount: QuantitativeInt
    amount: QuantitativeInt
    source_info: SourceInfo | None = None


class PriceList(CallbackCache):
    self: DatabaseMetaObject
    price_items: list[PriceItem]


class Invoice(CallbackCache, prefix='inv'):
    self: DatabaseMetaObject
    subscription: DatabaseMetaObject
    counterparty: DatabaseMetaObject
    tariff: DatabaseMetaObject
    deadline: datetime
    price: QuantitativeInt
    discount: QuantitativeInt
    amount: QuantitativeInt


class SuccessfulPayment(CallbackCache, prefix='pay'):
    invoice: DatabaseMetaObject
    timestamp: datetime


class InvoiceStatus(CallbackCache, prefix='invs'):
    ok: bool
    error_message: str | None


class StartSubscriptionInfo(CallbackCache, prefix='ssif'):
    next_payment_datetime: datetime
    period_text: str
    vpn_conf: str


class UpdateOffer(CallbackCache):
    expires_datetime: datetime
    item: PriceItem


class SubscriberInfo(CallbackCache, prefix='suif'):
    is_subscribed: bool
    update_offer: UpdateOffer | None
