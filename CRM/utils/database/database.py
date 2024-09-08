from . import brom_client
from datetime import datetime


def get_basic_tariffs_by_current_date():
    price = brom_client.ВызватьМетод("СоединениеБром", "ПолучитьОсновнойПрайсЛистНаДату")
    if price is not None:
        return price.Тарифы
    else:
        return None
