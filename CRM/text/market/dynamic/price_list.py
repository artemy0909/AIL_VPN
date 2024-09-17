from model.views import PriceList
from text.symbols import Emoji


def promo_code_activation(price_list: PriceList):
    text = f"<b>{Emoji.confetti} Промокод успешно активирован!</b>\n"
    text += "Теперь вы можете воспользоваться следующими тарифами со скидкой:\n\n"

    for item in price_list.price_items:
        if item.discount.value > 0:
            text += f"<b>{item.title}</b> — <s>{item.price}</s> ➡ {item.amount} (скидка {item.discount})\n"
        else:
            text += f"<b>{item.title}</b> — {item.amount}\n"

    return text
