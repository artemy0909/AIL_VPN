# from decimal import Decimal
#
# from model.views import PriceList, PriceItem, QuantitativeInt, SourceInfo
# from text.symbols import Symbols
#
#
# def to_price_item(price_item_obj, promo_code: SourceInfo = None) -> PriceItem:
#     return PriceItem(
#         title=price_item_obj.Тариф.НаименованиеДляБота,
#         tariff_guid=price_item_obj.Тариф.УникальныйИдентификатор(),
#         price=to_quantitative_int(value=price_item_obj.Стоимость, unit_symbol=Symbols.RUBBLE),
#         discount=to_quantitative_int(value=price_item_obj.Скидка, unit_symbol=Symbols.PERCENT),
#         amount=to_quantitative_int(value=price_item_obj.Сумма, unit_symbol=Symbols.RUBBLE),
#         promo_code=promo_code
#     )
#
#
# def to_quantitative_int(value: float, unit_symbol: str, semicolons: int = 2) -> QuantitativeInt:
#     value: int = int(Decimal(str(value)) * (10 ** semicolons))
#     return QuantitativeInt(value=value, unit_symbol=unit_symbol, semicolons=semicolons)
#
#
# def to_price_list(price_list_obj) -> PriceList:
#     price_items = []
#     for item in price_list_obj.Тарифы:
#         price_items.append(to_price_item(item))
#     return PriceList(price_items=price_items)
#
#
# def to_discount_price_list(price_list_obj, promo_code_str: str) -> PriceList:
#     promo_code = SourceInfo(
#         promo_code=promo_code_str,
#         refer_guid=price_list_obj.Реферал.УникальныйИдентификатор(),
#         source_guid=price_list_obj.ИсточникПодписки.УникальныйИдентификатор()
#     )
#     price_items = []
#     for item in price_list_obj.ПрайсЛист.Тарифы:
#         price_items.append(to_price_item(item, promo_code))
#     return PriceList(price_items=price_items)
