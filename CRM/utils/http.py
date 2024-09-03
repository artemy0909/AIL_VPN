import json
from dataclasses import dataclass

import requests


@dataclass
class ProductInfo:
    article: str
    title: str
    rating: float
    _price: int
    quantity: int

    @property
    def price(self):
        return f"{self._price // 100}.{self._price % 100} ₽"


def get_product_info(article: str) -> ProductInfo | None:
    request = requests.get(f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={article}")
    if request.status_code == 200:
        try:
            data = json.loads(request.content)["data"]["products"][0]
            total_quantity = 0
            for sizes in data["sizes"]:
                for stocks in sizes["stocks"]:
                    total_quantity += stocks["qty"]
            return ProductInfo(
                article=article,
                title=data["name"],
                rating=data["reviewRating"],
                _price=data['salePriceU'],
                quantity=total_quantity
            )
        except (KeyError, IndexError):
            return
    return
