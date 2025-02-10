from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ..states import Start
from keyboard import market as keyboard
from model.views import PriceList
from text import market as text
from utils.database import database


start_router = Router()


@start_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:

    user_info = database.get_or_create_user(telegram_id=message.from_user.id, full_name=message.from_user.full_name)

    price_list: PriceList = database.get_basic_price_list()

    await message.answer(
        text=text.hello_customer(name=message.from_user.full_name),
        reply_markup=keyboard.inline.price_list_keyboard(price_list))
    await state.set_state(Start.wait_to_promo_code)


@start_router.message(Start.wait_to_promo_code)
async def promo_code_activation(message: Message) -> None:

    promo_code_info: PriceList = database.get_promo_code_info(message.text)

    if promo_code_info:
        await message.answer(
            text=text.promo_code_activation(promo_code_info),
            reply_markup=keyboard.inline.price_list_keyboard(promo_code_info))
    else:
        await message.answer(
            text=text.PROMOCODE_NOT_FOUND)
