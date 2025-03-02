from aiogram import types, Router, F
from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, PreCheckoutQuery, Message, BufferedInputFile

from loader import market_bot
from model.views import PriceItem, Invoice, StartSubscriptionInfo
from utils.config import Config
from utils.database import database
from utils.database.xenon import XenonConnectionError

payment_router = Router()


@payment_router.callback_query(PriceItem.filter())
async def tariff_choice(query: CallbackQuery, callback_data: PriceItem):

    # subscriber_info: SubscriberInfo = database.get_subscriber_info(telegram_id=query.from_user.id)

    # if subscriber_info.is_subscribed and not subscriber_info.payment_method_id == Config.MAIN_PAYMENT_METHOD:
    #     await query.answer("Вы уже подписаны на этот тариф", show_alert=True)
    #
    # else:
        if Config.PAYMENT_TOKEN.split(':')[1] == 'TEST':
            await query.answer("Тестовый платеж!!!")

        invoice: Invoice = database.create_invoice(
            telegram_id=query.from_user.id, selected_item=callback_data, payment_method_id=Config.MAIN_PAYMENT_METHOD)

        price = types.LabeledPrice(label=callback_data.title, amount=callback_data.amount.value)

        await query.message.answer_invoice(
            title="Подписка на VPN",
            description="Ваша безопасность и доступ к ресурсам всего мира.",
            provider_token=Config.PAYMENT_TOKEN,
            currency=callback_data.amount.currency,
            photo_url=Config.PAYMENT_IMAGE_URL,
            photo_width=416,
            photo_height=234,
            photo_size=416,
            is_flexible=False,
            prices=[price],
            # start_parameter="one-month-subscription",
            protect_content=True,
            payload=invoice.pack())


@payment_router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    try:
        invoice: Invoice = Invoice.unpack(pre_checkout_q.invoice_payload)
        invoice_status = database.check_invoice(invoice=invoice)
    except XenonConnectionError as error:
        await market_bot.answer_pre_checkout_query(
            pre_checkout_q.id, ok=False, error_message="Произошла ошибка при обработке платежа, уже исправляем")

    else:
        await market_bot.answer_pre_checkout_query(
            pre_checkout_q.id, ok=invoice_status.ok, error_message=invoice_status.error_message)


@payment_router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    try:
        invoice: Invoice = Invoice.unpack(message.successful_payment.invoice_payload)
        subscription_info: StartSubscriptionInfo = database.payment_success(invoice=invoice)
    except XenonConnectionError as error:
        raise error
        # todo отработку ошибки
        # todo добавить отправку ошибки админу
    else:

        conf_bytes = subscription_info.conf_file.encode("utf-8")

        document = BufferedInputFile(
            file=conf_bytes,
            filename=subscription_info.conf_name
        )

        await message.answer_document(
            document=document,
            caption=f"Вы подписались на {subscription_info.period_text}"
                    f", следующая дата оплаты: {subscription_info.next_payment_datetime}. *инструкция по подписке*")
