from aiogram import types, Router, F
from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, PreCheckoutQuery, Message

from loader import market_bot
from model.views import PriceItem, Invoice
from utils.config import Config
from utils.database import database
from utils.database.xenon import XenonConnectionError

payment_router = Router()


@payment_router.callback_query(PriceItem.filter())
async def tariff_choice(query: CallbackQuery, callback_data: PriceItem):
    if Config.PAYMENT_TOKEN.split(':')[1] == 'TEST':
        await query.answer("Тестовый платеж!!!")

    invoice: Invoice = database.create_invoice(telegram_id=query.from_user.id, selected_item=callback_data)

    price = types.LabeledPrice(label=callback_data.title, amount=callback_data.amount.value)

    await query.message.answer_invoice(
        title="Подписка на VPN",
        description="Ваша безопасность и доступ к ресурсам всего мира.",
        provider_token=Config.PAYMENT_TOKEN,
        currency=callback_data.amount.currency,
        # photo_url="https://i.pinimg.com/originals/e1/4c/a2/e14ca245e887f57fbb9acbdacf8d74ca.jpg",
        # photo_width=416,
        # photo_height=234,
        # photo_size=416,
        is_flexible=False,
        prices=[price],
        start_parameter="one-month-subscription",
        payload=invoice.pack())


@payment_router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    try:
        invoice: Invoice = Invoice.unpack(pre_checkout_q.invoice_payload)
        invoice_status = database.check_invoice(invoice=invoice)
    except XenonConnectionError:
        await market_bot.answer_pre_checkout_query(
            pre_checkout_q.id, ok=False, error_message="Произошла ошибка при обработке платежа")
    else:
        await market_bot.answer_pre_checkout_query(
            pre_checkout_q.id, ok=invoice_status.ok, error_message=invoice_status.error_message)


@payment_router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    await market_bot.send_message(
        message.chat.id,
        f"Платеж на сумму {message.successful_payment.total_amount // 100}"
        f" {message.successful_payment.currency} прошел успешно!!!")
