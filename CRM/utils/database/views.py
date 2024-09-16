from . import call_method
from .models import PriceItem, PromoCodeInfo, PriceList


# def get_counterparty(telegram_id: str):
#     return call_method("ПолучитьКонтрагентаСессии").УникальныйИдентификатор()

def get_basic_price_list() -> PriceList:
    price_list = call_method("ПолучитьОсновнойПрайсЛистНаДату")

    if price_list is not None:
        return PriceList(price_list)


def get_promo_code_info(promo_code: str) -> PromoCodeInfo:
    promo_code_info = call_method("ПолучитьДанныеПоПромокоду", promo_code)

    if promo_code_info is not None:
        return PromoCodeInfo(promo_code_info, promo_code)
