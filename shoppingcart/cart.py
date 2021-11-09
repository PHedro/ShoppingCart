import typing
from collections import OrderedDict

from . import abc


class ShoppingCart(abc.ShoppingCart):
    def __init__(self):
        self._items = OrderedDict()

    def add_item(self, product_code: str, quantity: int):
        quantity += self._items.get(product_code, 0)
        self._items.update({product_code: quantity})

    def print_receipt(self) -> typing.List[str]:
        lines = []

        for product, quantity in self._items.items():
            price = self._get_product_price(product) * quantity

            lines.append("{product} - {quantity} - {price_string}".format(
                product=product,
                quantity=str(quantity),
                price_string="€%.2f" % price
            ))

        return lines

    def _get_product_price(self, product_code: str) -> float:
        price = 0.0

        if product_code == "apple":
            price = 1.0

        elif product_code == "banana":
            price = 1.1

        elif product_code == "kiwi":
            price = 3.0

        return price
