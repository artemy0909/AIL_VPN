from aiogram import F
from aiogram import types, Router
from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram.types import CallbackQuery, PreCheckoutQuery, Message

from keyboard.callbacks import TariffChoiceCallback
from loader import market_bot
from utils.config import Config

payment_router = Router()


@payment_router.callback_query(TariffChoiceCallback.filter())
async def tariff_choice(query: CallbackQuery, callback_data: TariffChoiceCallback):
    await query.answer("test")


@payment_router.message(Command('buy'))
async def buy(message: types.Message):
    if Config.PAYMENT_TOKEN.split(':')[1] == 'TEST':
        await message.answer("Тестовый платеж!!!")

    PRICE = types.LabeledPrice(label="Подписка на месяц", amount=500 * 100)

    await message.answer_invoice(
        title="VPN на месяц",
        description="Ваша безопасность и доступ к ресурсам всего мира.",
        provider_token=Config.PAYMENT_TOKEN,
        currency="rub",
        photo_url="https://i.pinimg.com/originals/e1/4c/a2/e14ca245e887f57fbb9acbdacf8d74ca.jpg",
        # photo_width=416,
        # photo_height=234,
        # photo_size=416,
        is_flexible=False,
        prices=[PRICE],
        start_parameter="one-month-subscription",
        payload="test-invoice-payload")


@payment_router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    await market_bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@payment_router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    await market_bot.send_message(
        message.chat.id,
        f"Платеж на сумму {message.successful_payment.total_amount // 100}"
        f" {message.successful_payment.currency} прошел успешно!!!")
