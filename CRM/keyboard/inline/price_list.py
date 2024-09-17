from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from model.views import PriceList, PriceItem


def basic_prices(price_list: PriceList) -> InlineKeyboardMarkup:

    keyboard_builder = InlineKeyboardBuilder()
    for price_item in price_list.price_items:
        keyboard_builder.button(
            text=str(price_item),
            callback_data=PriceItem(
                tariff_guid=price_item.tariff_guid,
                amount=price_item.amount.value,
                price=price_item.price,
                discount=price_item.discount,
            ))

    keyboard_builder.adjust(1)

    return keyboard_builder.as_markup()


def promo_code_prices(price_list: PriceList) -> InlineKeyboardMarkup:

    keyboard_builder = InlineKeyboardBuilder()
    pass # todo
