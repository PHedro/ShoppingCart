import json
import typing
from collections import OrderedDict

from . import abc
from .constants import PRODUCTS, CURRENCY


class ShoppingCartFactory:
    prices = dict()
    currency = "€"

    def __init__(self, configuration_json: str):
        self.load_configurations(configuration_json=configuration_json)

    def load_configurations(self, configuration_json: str):
        with open(configuration_json) as config_file:
            loaded_data = json.load(config_file)
        self.prices = loaded_data.get(PRODUCTS)
        self.currency = loaded_data.get(CURRENCY, "€")

    def create_shopping_cart(self):
        return ShoppingCart(prices=self.prices, currency=self.currency)


class ShoppingCart(abc.ShoppingCart):
    def __init__(self, prices: dict, currency: str):
        self._items = OrderedDict()
        self.receipt = []
        self.total_price = 0.0
        self.currency = currency
        self.prices_cached = prices

    def add_item(self, product_code: str, quantity: int):
        # thought on changing the quantity to float to better represent
        # items that are sold in fractions (i.e. 1.5kg of meat) keeping int
        # to follow the abstract class
        quantity += self._items.get(product_code, 0)
        self._items.update({product_code: quantity})

    def print_receipt(self) -> typing.List[str]:
        self._receipt_entries()

        return self.receipt

    def _reset_cached_values(self):
        self.receipt = []
        self.total_price = 0.0

    def _total_entry(self):
        total_entry = "TOTAL - - - {total_price_string}".format(
            total_price_string="%s%.2f" % (self.currency, self.total_price)
        )
        self.receipt.append(total_entry)
        return total_entry

    def _receipt_entries(self):
        self._reset_cached_values()
        for product, quantity in self._items.items():
            price = self._get_product_price(product) * quantity
            self.total_price += price

            self.receipt.append("{product} - {quantity} - {price_string}".format(
                product=product,
                quantity=quantity,
                price_string="%s%.2f" % (self.currency, price)
            ))

        self._total_entry()
        return self.receipt, self.total_price

    def _get_product_price(self, product_code: str) -> float:
        return self.prices_cached.get(product_code, 0.0)
