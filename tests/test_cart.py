from unittest import TestCase

from shoppingcart.cart import ShoppingCart


class ShoppingCartTestCase(TestCase):
    def setUp(self):
        self.cart = ShoppingCart()

    def test_add_item(self):
        self.cart.add_item("apple", 1)

        receipt = self.cart.print_receipt()

        self.assertEqual(receipt[0], "apple - 1 - €1.00")
        self.assertEqual(receipt[1], "TOTAL - - - €1.00")

    def test_add_item_with_multiple_quantity(self):
        self.cart.add_item("apple", 2)

        receipt = self.cart.print_receipt()

        self.assertEqual(receipt[0], "apple - 2 - €2.00")
        self.assertEqual(receipt[1], "TOTAL - - - €2.00")

    def test_add_different_items(self):
        self.cart.add_item("banana", 1)
        self.cart.add_item("kiwi", 1)

        receipt = self.cart.print_receipt()

        self.assertEqual(receipt[0], "banana - 1 - €1.10")
        self.assertEqual(receipt[1], "kiwi - 1 - €3.00")
        self.assertEqual(receipt[2], "TOTAL - - - €4.10")

    def test_receipt_ordering(self):
        self.cart.add_item("banana", 1)
        self.cart.add_item("kiwi", 1)
        self.cart.add_item("banana", 1)
        self.cart.add_item("apple", 1)

        receipt = self.cart.print_receipt()

        self.assertEqual(receipt[0], "banana - 2 - €2.20")
        self.assertEqual(receipt[1], "kiwi - 1 - €3.00")
        self.assertEqual(receipt[2], "apple - 1 - €1.00")
        self.assertEqual(receipt[3], "TOTAL - - - €6.20")

    def test_generate_receipt_entries(self):
        self.cart.add_item("banana", 1)
        self.cart.add_item("kiwi", 1)
        self.cart.add_item("banana", 1)
        self.cart.add_item("apple", 1)

        receipt, _ = self.cart._receipt_entries()

        self.assertEqual(receipt[0], "banana - 2 - €2.20")
        self.assertEqual(receipt[1], "kiwi - 1 - €3.00")
        self.assertEqual(receipt[2], "apple - 1 - €1.00")
        self.assertEqual(receipt[3], "TOTAL - - - €6.20")

    def test_generate_total_entry(self):
        self.cart.add_item("banana", 1)
        self.cart.add_item("kiwi", 1)
        self.cart.add_item("banana", 1)
        self.cart.add_item("apple", 1)
        _, total_price = self.cart._receipt_entries()
        total = self.cart._total_entry()

        self.assertEqual(total, "TOTAL - - - €6.20")

    def test_reset_cached_values(self):
        self.cart.add_item("banana", 1)
        self.cart.add_item("kiwi", 1)
        self.cart.add_item("banana", 1)
        self.cart.add_item("apple", 1)
        _, total_price = self.cart._receipt_entries()
        self.cart._reset_cached_values()

        self.assertEqual(0.0, self.cart.total_price)
        self.assertEqual(0, len(self.cart.receipt))
