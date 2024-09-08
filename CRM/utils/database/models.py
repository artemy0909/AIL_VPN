from decimal import Decimal

class Symbols:
    RUBBLE = "₽"
    PERCENT = "%"

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

class PriceItem:

    def __init__(self, tariff_object):
        self.title = tariff_object.Тариф.НаименованиеДляБота
        self.tariff_guid = tariff_object.Тариф.УникальныйИдентификатор()
        self.price = QuantitativeInt(tariff_object.Стоимость, unit_symbol=Symbols.RUBBLE)
        self.discount = QuantitativeInt(tariff_object.Скидка, unit_symbol=Symbols.PERCENT)
        self.amount = QuantitativeInt(tariff_object.Сумма, unit_symbol=Symbols.RUBBLE)

