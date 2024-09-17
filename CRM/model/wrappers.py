from model.views import PriceList, PriceItem, QuantitativeInt, PromoCode
from text.symbols import Units


def to_price_item(price_item_obj, promo_code: PromoCode = None) -> PriceItem:
    return PriceItem(
        title=price_item_obj.Тариф.НаименованиеДляБота,
        tariff_guid=price_item_obj.Тариф.УникальныйИдентификатор(),
        price=QuantitativeInt(value=price_item_obj.Стоимость, unit_symbol=Units.RUBBLE),
        discount=QuantitativeInt(value=price_item_obj.Скидка, unit_symbol=Units.PERCENT),
        amount=QuantitativeInt(value=price_item_obj.Сумма, unit_symbol=Units.RUBBLE),
        promo_code=promo_code
    )


def to_price_list(price_list_obj) -> PriceList:
    price_items = []
    for item in price_list_obj.Тарифы:
        price_items.append(to_price_item(item))
    return PriceList(price_items=price_items)


def to_discount_price_list(price_list_obj, promo_code_str: str) -> PriceList:
    promo_code = PromoCode(
        promo_code=promo_code_str,
        refer_guid=price_list_obj.Реферал.УникальныйИдентификатор(),
        source_guid=price_list_obj.Источник.УникальныйИдентификатор()
    )
    price_items = []
    for item in price_list_obj.ПрайсЛист.Тарифы:
        price_items.append(to_price_item(item, promo_code))
    return PriceList(price_items=price_items)
