from dataclasses import dataclass

from keyboard.inline import price_list


@dataclass
class Start:
    basic_prices: callable = price_list.basic_prices
    promo_code_prices: callable = price_list.promo_code_prices
