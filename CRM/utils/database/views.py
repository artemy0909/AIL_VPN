from . import database
from .models import PriceItem


def get_basic_price_list_for_keyboard() -> list[PriceItem]:
    basic_tariffs = database.get_basic_tariffs_by_current_date()

    result = []
    for tariff in basic_tariffs:
        result.append(PriceItem(tariff))

    return result
