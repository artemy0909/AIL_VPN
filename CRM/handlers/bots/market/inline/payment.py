from mailbox import Message

from aiogram import Router
from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, PreCheckoutQuery

from keyboard.callbacks import PriceChoiceCallback
from loader import market_bot

payment_router = Router()


@payment_router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    await market_bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@payment_router.message(content_type=ContentType.SUCCESSFUL_PAYMENT)  # todo разобраться что тут писать
async def successful_payment(message: Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    await market_bot.send_message(message.chat.id,
                                  f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!")


@payment_router.callback_query(PriceChoiceCallback.filter())
async def price_choice(query: CallbackQuery, callback_data: PriceChoiceCallback):
    await query.answer()


# prices
from aiogram import types, Router
from aiogram.filters import Command

from utils.config import Config

PRICE = types.LabeledPrice(label="Подписка на 1 месяц", amount=500 * 100)

payment_router = Router()


@payment_router.message(Command('buy'))
async def buy(message: types.Message):
    if Config.PAYMENT_TOKEN.split(':')[1] == 'TEST':
        await message.answer("Тестовый платеж!!!")

    await message.answer_invoice(
        title="Подписка на месяц",
        description="Ваша безопасность и доступ к ресурсам всего мира.",
        provider_token=Config.PAYMENT_TOKEN,
        currency="rub",
        photo_url="https://i.pinimg.com/originals/e1/4c/a2/e14ca245e887f57fbb9acbdacf8d74ca.jpg",
        # photo_width=416,
        # photo_height=234,
        # photo_size=416,
        # is_flexible=False,
        prices=[PRICE],
        start_parameter="one-month-subscription",
        payload="test-invoice-payload")
