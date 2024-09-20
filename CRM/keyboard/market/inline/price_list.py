from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from model.views import PriceList
from text.market import price_item_label


def price_list_keyboard(price_list: PriceList) -> InlineKeyboardMarkup:

    keyboard_builder = InlineKeyboardBuilder()
    for price_item in price_list.price_items:
        keyboard_builder.button(
            text=price_item_label(price_item),
            callback_data=price_item)

    keyboard_builder.adjust(1)

    return keyboard_builder.as_markup()

