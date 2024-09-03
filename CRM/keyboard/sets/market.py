from dataclasses import dataclass


@dataclass
class Start:
    basic_prices: callable = basic_prices