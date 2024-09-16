from dataclasses import dataclass

from ..dynamic import start, price_list


@dataclass
class Start:
    hello_customer: callable = start.hello_customer
    promo_code_activation: callable = price_list.promo_code_activation
