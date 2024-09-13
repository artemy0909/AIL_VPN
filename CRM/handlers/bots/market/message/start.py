from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboard.sets.market import Start as Keyboard

start_router = Router()


@start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        text="test",
        reply_markup=Keyboard.test()
    )

    # await message.answer(
    #     text=Text.hello_customer(name=message.from_user.full_name),
    #     reply_markup=Keyboard.basic_prices())
