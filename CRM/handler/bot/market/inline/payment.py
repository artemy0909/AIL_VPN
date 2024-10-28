from aiogram import types, Router, F
from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram.types import CallbackQuery, PreCheckoutQuery, Message

from loader import market_bot
from model.views import PriceItem
from utils.config import Config

payment_router = Router()


@payment_router.callback_query(PriceItem.filter())
async def tariff_choice(query: CallbackQuery, callback_data: PriceItem):
    if Config.PAYMENT_TOKEN.split(':')[1] == 'TEST':
        await query.answer("Тестовый платеж!!!")

    invoice: Invoice = database.get_basic_price_list()

    price = types.LabeledPrice(label=callback_data.title, amount=callback_data.amount.value)

    await query.message.answer_invoice(
        title="Подписка на VPN",
        description="Ваша безопасность и доступ к ресурсам всего мира.",
        provider_token=Config.PAYMENT_TOKEN,
        currency="rub",
        # photo_url="https://i.pinimg.com/originals/e1/4c/a2/e14ca245e887f57fbb9acbdacf8d74ca.jpg",
        # photo_width=416,
        # photo_height=234,
        # photo_size=416,
        is_flexible=False,
        prices=[price],
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
