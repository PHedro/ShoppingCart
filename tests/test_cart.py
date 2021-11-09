from unittest import TestCase

from shoppingcart.cart import ShoppingCart


class ShoppingCartTestCase(TestCase):
    def setUp(self):
        self.cart = ShoppingCart()

    def test_add_item(self):
        self.cart.add_item("apple", 1)

        receipt = self.cart.print_receipt()

        assert receipt[0] == "apple - 1 - €1.00"

    def test_add_item_with_multiple_quantity(self):
        self.cart.add_item("apple", 2)

        receipt = self.cart.print_receipt()

        assert receipt[0] == "apple - 2 - €2.00"

    def test_add_different_items(self):
        self.cart.add_item("banana", 1)
        self.cart.add_item("kiwi", 1)

        receipt = self.cart.print_receipt()

        assert receipt[0] == "banana - 1 - €1.10"
        assert receipt[1] == "kiwi - 1 - €3.00"

    def test_receipt_ordering(self):
        self.cart.add_item("banana", 1)
        self.cart.add_item("kiwi", 1)
        self.cart.add_item("banana", 1)
        self.cart.add_item("apple", 1)

        receipt = self.cart.print_receipt()

        assert receipt[0] == "banana - 2 - €2.20"
        assert receipt[1] == "kiwi - 1 - €3.00"
        assert receipt[2] == "apple - 1 - €1.00"
