from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboard.sets.market import Start as Keyboard
from text.sets.market import Start as Text

start_router = Router()


@start_router.message(CommandStart())
async def command_start(message: Message) -> None:
    await message.answer(
        text=Text.hello_customer(name=message.from_user.full_name),
        reply_markup=Keyboard.basic_prices())


@start_router.message()
async def promo_code_activation(message: Message) -> None:
    get_promo_code_info(message.text)
    await message.answer()