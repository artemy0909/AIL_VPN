from model.views import PriceList, PriceItem
from text.symbols import Emoji


def promo_code_activation(price_list: PriceList):
    text = f"<b>{Emoji.CONFFETI} Промокод успешно активирован!</b>\n\n"
    text += "Теперь вы можете воспользоваться следующими тарифами со скидкой:\n\n"

    for item in price_list.price_items:
        if item.discount.value > 0:
            text += (f"{Emoji.STAR} <b>{item.title}</b>:\n"
                     f" <s>{item.price}</s> {item.amount} (-{item.discount})\n")
        # else:
        #     text += f"{Emoji.STAR} <b>{item.title}</b>:\n {item.amount}\n"

    return text


def price_item_label(price_item: PriceItem):
    return f"{price_item.title} ({price_item.amount})"
