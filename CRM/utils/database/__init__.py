from model.views import PriceList
from model.wrappers import to_price_list, to_discount_price_list
from .connection import BromClientWrapper


# def get_counterparty(telegram_id: str):
#     return call_method("ПолучитьКонтрагентаСессии").УникальныйИдентификатор()
class Database(BromClientWrapper):
    def get_basic_price_list(self) -> PriceList:
        price_list = self._call_method("ПолучитьОсновнойПрайсЛистНаДату")

        if price_list is not None:
            return to_price_list(price_list)

    def get_promo_code_info(self, promo_code: str) -> PriceList:
        promo_code_info = self._call_method("ПолучитьДанныеПоПромокоду", promo_code)

        if promo_code_info is not None:
            return to_discount_price_list(promo_code_info, promo_code)

    def create_counterparty(self):
        self._call_method("СоздатьСессиюЕслиНовая")
