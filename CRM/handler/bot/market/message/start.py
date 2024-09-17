from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboard.set.market import Start as Keyboard
from model.views import PriceList, PromoCode
from text.set.market import Start as Text
from utils import database

start_router = Router()


@start_router.message(CommandStart())
async def command_start(message: Message) -> None:

    price_list: PriceList = database.get_basic_price_list()

    await message.answer(
        text=Text.hello_customer(name=message.from_user.full_name),
        reply_markup=Keyboard.basic_prices(price_list))


@start_router.message()
async def promo_code_activation(message: Message) -> None:

    promo_code_info: PromoCode = database.get_promo_code_info(message.text)

    if promo_code_info:
        await message.answer(
            text=Text.promo_code_activation(promo_code_info),
            reply_markup=Keyboard.promo_code_prices(promo_code_info))
    else:
        pass

