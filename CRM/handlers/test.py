# prices
from aiogram import types, Router
from aiogram.filters import Command

PRICE = types.LabeledPrice(label="Подписка на 1 месяц", amount=500 * 100)

PAYMENT_TOKEN = "381764678:TEST:91506"

payment_router = Router()


@payment_router.message(Command('buy'))
async def buy(message: types.Message):
    if PAYMENT_TOKEN.split(':')[1] == 'TEST':
        await message.answer("Тестовый платеж!!!")

    await message.answer_invoice(
        title="Ежемесячная подписка на VPN",
        description="Ваша безопасность и доступ к ресурсам всего мира.",
        provider_token=PAYMENT_TOKEN,
        currency="rub",
        photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
        # photo_width=416,
        # photo_height=234,
        # photo_size=416,
        # is_flexible=False,
        prices=[PRICE],
        start_parameter="one-month-subscription",
        payload="test-invoice-payload")
