from decimal import Decimal

from text.symbols import Emoji, Units


class QuantitativeInt:
    def __init__(self, value: float, unit_symbol: str, semicolons: int = 2):
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


class PriceList:

    def __init__(self, price_list_object):
        self.price_items = []
        for tariff in price_list_object.Тарифы:
            self.price_items.append(PriceItem(tariff))


class PriceItem:  # todo объеденить с callbacks

    def __init__(self, tariff_object):
        self.title = tariff_object.Тариф.НаименованиеДляБота
        self.tariff_guid = tariff_object.Тариф.УникальныйИдентификатор()
        self.price = QuantitativeInt(tariff_object.Стоимость, unit_symbol=Units.RUBBLE)
        self.discount = QuantitativeInt(tariff_object.Скидка, unit_symbol=Units.PERCENT)
        self.amount = QuantitativeInt(tariff_object.Сумма, unit_symbol=Units.RUBBLE)

    def __str__(self):
        return f"{Emoji.star} {self.title} - {self.amount}"


class PromoCodeInfo:

    def __init__(self, promo_code_info_object, promo_code_str):
        self.promo_code = promo_code_str
        self.price_items = []
        for tariff in promo_code_info_object.ПрайсЛист:
            self.price_items.append(PriceItem(tariff))
        self.referral_guid = promo_code_info_object.Реферал.УникальныйИдентификатор()
        self.source_guid = promo_code_info_object.ИсточникПодписки.УникальныйИдентификатор()
