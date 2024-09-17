from model.views import PriceList, PromoCode
from model.wrappers import to_price_list, to_promo_code
from .connection import call_method


# def get_counterparty(telegram_id: str):
#     return call_method("ПолучитьКонтрагентаСессии").УникальныйИдентификатор()

def get_basic_price_list() -> PriceList:
    price_list = call_method("ПолучитьОсновнойПрайсЛистНаДату")

    if price_list is not None:
        return to_price_list(price_list)


def get_promo_code_info(promo_code: str) -> PromoCode:
    promo_code_info = call_method("ПолучитьДанныеПоПромокоду", promo_code)

    if promo_code_info is not None:
        return to_promo_code(promo_code_info, promo_code)
