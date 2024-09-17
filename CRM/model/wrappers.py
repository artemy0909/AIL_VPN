from model.views import PriceList, PriceItem, QuantitativeInt, PromoCode
from text.symbols import Units


def to_price_item(price_item_obj) -> PriceItem:
    return PriceItem(
        title=price_item_obj.Тариф.НаименованиеДляБота,
        tariff_guid=price_item_obj.Тариф.УникальныйИдентификатор(),
        price=QuantitativeInt(value=price_item_obj.Стоимость, unit_symbol=Units.RUBBLE),
        discount=QuantitativeInt(value=price_item_obj.Скидка, unit_symbol=Units.PERCENT),
        amount=QuantitativeInt(value=price_item_obj.Сумма, unit_symbol=Units.RUBBLE)
    )


def to_price_list(price_list_obj) -> PriceList:
    price_items = []
    for item in price_list_obj.Тарифы:
        price_items.append(to_price_item(item))
    return PriceList(price_items=price_items)


def to_promo_code(promo_code_info, promo_code: str) -> PromoCode:
    return PromoCode(
        promo_code=promo_code,
        refer_guid=promo_code_info.Реферал.УникальныйИдентификатор(),
        source_guid=promo_code_info.ИсточникПодписки.УникальныйИдентификатор()
    )
