from io import BytesIO

import qrcode
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BufferedInputFile

from keyboard import market as keyboard
from model.views import PriceList, StartSubscriptionInfo
from text import market as text
from utils.database import database
from ..states import Start

start_router = Router()


@start_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:

    args = message.text.split(" ")
    if len(args) > 1:

        wait_message = await message.answer("Проверяем промокод...")
        database.get_or_create_user(telegram_id=message.from_user.id, full_name=message.from_user.full_name)

        answer = database.get_promo_code_info(telegram_id=message.from_user.id, promo_code=args[1])

        if isinstance(answer, StartSubscriptionInfo):
            conf_text = answer.conf.data
            conf_bytes = conf_text.encode("utf-8")

            qr = qrcode.make(conf_text)
            qr_io = BytesIO()
            qr.save(qr_io, format="PNG")
            qr_io.seek(0)

            qr_photo = BufferedInputFile(qr_io.getvalue(), filename="qr_code.png")

            document = BufferedInputFile(
                file=conf_bytes,
                filename=answer.conf.name
            )
            await message.answer_photo(qr_photo)
            await message.answer_document(document, caption=text.FREE_PROMOCODE_ACTIVATED)
            await wait_message.delete()

        else:
            await wait_message.edit_text("Не удалось верифицировать промокод")

#     else:
#
#         price_list: PriceList = database.get_basic_price_list()
#
#         await message.answer(
#             text=text.hello_customer(name=message.from_user.full_name),
#             reply_markup=keyboard.inline.price_list_keyboard(price_list),
#             disable_web_page_preview=True)
#         await state.set_state(Start.wait_to_promo_code)
#
#
# @start_router.message(Start.wait_to_promo_code)
# async def promo_code_activation(message: Message) -> None:
#     promo_code_info: PriceList = database.get_promo_code_info(message.text)
#
#     if promo_code_info:
#         await message.answer(
#             text=text.promo_code_activation(promo_code_info),
#             reply_markup=keyboard.inline.price_list_keyboard(promo_code_info))
#     else:
#         await message.answer(
#             text=text.PROMOCODE_NOT_FOUND)
