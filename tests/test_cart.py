from unittest import TestCase

from shoppingcart.cart import ShoppingCart, ShoppingCartFactory


class ShoppingCartFactoryTestCase(TestCase):
    def setUp(self):
        self.factory = ShoppingCartFactory("prices.json")

    def test_load_data_correctly(self):
        self.factory.load_configurations("prices.json")
        self.assertEqual("€", self.factory.currency)
        self.assertEqual(1.0, self.factory.prices.get("apple"))
        self.assertEqual(1.1, self.factory.prices.get("banana"))
        self.assertEqual(3.0, self.factory.prices.get("kiwi"))

    def test_create_cart_with_data_correctly(self):
        self.factory.load_configurations("prices.json")

        cart = self.factory.create_shopping_cart()
        self.assertEqual("€", cart.currency)
        self.assertEqual(1.0, cart.prices_cached.get("apple"))
        self.assertEqual(1.1, cart.prices_cached.get("banana"))
        self.assertEqual(3.0, cart.prices_cached.get("kiwi"))

    def test_create_multiple_carts_with_same_data(self):
        self.factory.load_configurations("prices.json")

        cart = self.factory.create_shopping_cart()
        self.assertEqual("€", cart.currency)
        self.assertEqual(1.0, cart.prices_cached.get("apple"))
        self.assertEqual(1.1, cart.prices_cached.get("banana"))
        self.assertEqual(3.0, cart.prices_cached.get("kiwi"))

        cart2 = self.factory.create_shopping_cart()
        self.assertEqual("€", cart2.currency)
        self.assertEqual(1.0, cart2.prices_cached.get("apple"))
        self.assertEqual(1.1, cart2.prices_cached.get("banana"))
        self.assertEqual(3.0, cart2.prices_cached.get("kiwi"))

    def test_create_multiple_carts_with_data_being_reloaded(self):
        self.factory.load_configurations("prices.json")

        cart = self.factory.create_shopping_cart()
        self.assertEqual("€", cart.currency)
        self.assertEqual(1.0, cart.prices_cached.get("apple"))
        self.assertEqual(1.1, cart.prices_cached.get("banana"))
        self.assertEqual(3.0, cart.prices_cached.get("kiwi"))

        cart2 = self.factory.create_shopping_cart()
        self.assertEqual("€", cart2.currency)
        self.assertEqual(1.0, cart2.prices_cached.get("apple"))
        self.assertEqual(1.1, cart2.prices_cached.get("banana"))
        self.assertEqual(3.0, cart2.prices_cached.get("kiwi"))

        self.factory.load_configurations("prices2.json")

        cart3 = self.factory.create_shopping_cart()
        self.assertEqual("£", cart3.currency)
        self.assertEqual(3.0, cart3.prices_cached.get("apple"))
        self.assertEqual(4.1, cart3.prices_cached.get("banana"))
        self.assertEqual(6.0, cart3.prices_cached.get("kiwi"))
        self.assertEqual(9.0, cart3.prices_cached.get("papaya"))


class ShoppingCartTestCase(TestCase):
    def setUp(self):
        self.prices = {
            "apple": 1.0,
            "banana": 1.1,
            "kiwi": 3.0
        }
        self.currency = "€"
        self.cart = ShoppingCart(
            prices=self.prices,
            currency=self.currency
        )

    def test_add_item(self):
        self.cart.add_item("apple", 1)

        receipt = self.cart.print_receipt()

        self.assertEqual(receipt[0], "apple - 1 - €1.00")
        self.assertEqual(receipt[1], "TOTAL - - - €1.00")

    def test_currency_as_pounds(self):
        cart = ShoppingCart(currency="£", prices=self.prices)
        cart.add_item("apple", 1)

        receipt = cart.print_receipt()

        self.assertEqual(receipt[0], "apple - 1 - £1.00")
        self.assertEqual(receipt[1], "TOTAL - - - £1.00")

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
