from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ..states import Start

from keyboard import market as keyboard
from model.views import PriceList
from text import service as text
from utils.database import database

start_router = Router()


@start_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await message.answer(text.hello_seller(name=message.from_user.full_name))
    await state.set_state(Start.waiting_for_token)


@start_router.message(Start.waiting_for_token)
async def token_auth(message: Message, state: FSMContext) -> None:
    auth_info = database.token_auth(telegram_id=message.text)
