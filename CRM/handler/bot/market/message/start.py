from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboard import market as keyboard
from model.views import PriceList
from text import market as text
from utils.database import database

start_router = Router()


@start_router.message(CommandStart())
async def command_start(message: Message) -> None:

    database.check_user_exist(telegram_id=message.from_user.id, full_name=message.from_user.full_name)

    price_list: PriceList = database.get_basic_price_list()

    await message.answer(
        text=text.hello_customer(name=message.from_user.full_name),
        reply_markup=keyboard.inline.price_list_keyboard(price_list))


@start_router.message()  # todo сделать что-нибудь от ложных срабатываний
async def promo_code_activation(message: Message) -> None:

    promo_code_info: PriceList = database.get_promo_code_info(message.text)

    if promo_code_info:
        await message.answer(
            text=text.promo_code_activation(promo_code_info),
            reply_markup=keyboard.inline.price_list_keyboard(promo_code_info))
    else:
        await message.answer(
            text=text.PROMOCODE_NOT_FOUND)
