from dataclasses import dataclass

from keyboard.inline import tariffs


@dataclass
class Start:
    basic_prices: callable = tariffs.basic_prices
    test: callable = tariffs.test
