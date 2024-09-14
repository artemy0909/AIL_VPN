from datetime import datetime

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboard.callbacks import TariffChoiceCallback
from utils.database import views
from utils.database.models import PriceItem


def basic_prices() -> InlineKeyboardMarkup:
    price_list: list[PriceItem] = views.get_basic_price_list_for_keyboard()

    keyboard_builder = InlineKeyboardBuilder()
    for price in price_list:
        keyboard_builder.button(
            text=f"⭐️ {price.title} - {price.amount}",
            callback_data=TariffChoiceCallback(
                tariff_guid=price.tariff_guid,
                amount=price.amount.value))

    keyboard_builder.adjust(1)

    return keyboard_builder.as_markup()
