from model.views import PriceList
from .xenon import XenonClient
from ..config import Config


# def get_counterparty(telegram_id: str):
#     return call_method("ПолучитьКонтрагентаСессии").УникальныйИдентификатор()
# class Database(BromClientWrapper):
#     def get_basic_price_list(self) -> PriceList:
#         price_list = self._call_method("ПолучитьОсновнойПрайсЛистНаДату")
#
#         if price_list is not None:
#             return to_price_list(price_list)
#
#     def get_promo_code_info(self, promo_code: str) -> PriceList:
#         promo_code_info = self._call_method("ПолучитьДанныеПоПромокоду", promo_code)
#
#         if promo_code_info is not None:
#             return to_discount_price_list(promo_code_info, promo_code)
#
#     def create_counterparty(self):
#         self._call_method("СоздатьСессиюЕслиНовая")

class Database(XenonClient):

    def get_basic_price_list(self) -> PriceList:
        response = self.get("pricelist")
        return PriceList.model_validate_json(response.text)

    def get_promo_code_info(self, promo_code: str) -> PriceList | None:
        response = self.get("promocode_info", promo_code=promo_code)
        if response.status_code == 204:
            return None
        else:
            return PriceList.model_validate_json(response.text)

    def create_counterparty(self):
        pass
        # self._call_method("СоздатьСессиюЕслиНовая")


database = Database(api_url=Config.XENON_API_URL, login=Config.XENON_LOGIN, password=Config.XENON_PASSWORD)
