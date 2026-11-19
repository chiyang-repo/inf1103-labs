import unittest
from supplier import Supplier
from product_factory import ProductFactory
from order import Order


class TestValidation(unittest.TestCase):
    def setUp(self) -> None: # Runs before every test
        self.supplier = Supplier(1, "Tech Supplies Inc.", "techsupplies@example.com")
        self.lamp = ProductFactory.create("physical", 1, "Desk Lamp", 25.00, 10, self.supplier, weight=1.2)

    def test_valid_product_is_created(self): # Good data still works
        self.assertEqual(self.lamp.get_price(), 25.00)
        self.assertEqual(self.lamp.get_stock(), 10)

    def test_zero_stock_is_allowed(self): # Boundary: 0 is not negative, so it is valid
        product = ProductFactory.create("digital", 2, "Old App", 9.99, 0, self.supplier)
        self.assertEqual(product.get_stock(), 0)

    def test_price_must_be_greater_than_zero(self):
        for bad_price in [0, -5.00]:
            with self.subTest(price=bad_price):
                with self.assertRaisesRegex(ValueError, "Price must be greater than zero"):
                    ProductFactory.create("physical", 3, "Bad Lamp", bad_price, 10, self.supplier)

    def test_stock_cannot_be_negative(self):
        with self.assertRaisesRegex(ValueError, "Stock quantity cannot be negative"):
            ProductFactory.create("physical", 4, "Chair", 49.90, -1, self.supplier)

    def test_digital_product_cannot_skip_stock_rule(self): # LSP: the child follows the parent's rule
        with self.assertRaisesRegex(ValueError, "Stock quantity cannot be negative"):
            ProductFactory.create("digital", 5, "Photo Editor", 49.90, -1, self.supplier)

    def test_order_line_quantity_must_be_greater_than_zero(self):
        order = Order(1)
        for bad_quantity in [0, -2]:
            with self.subTest(quantity=bad_quantity):
                with self.assertRaisesRegex(ValueError, "Quantity must be greater than zero"):
                    order.add_order_line(self.lamp, bad_quantity)
        self.assertEqual(len(order.get_order_lines()), 0) # Nothing was half-added

    def test_valid_order_line_still_works(self):
        order = Order(1)
        order.add_order_line(self.lamp, 2)
        self.assertEqual(len(order.get_order_lines()), 1)
        self.assertEqual(order.calculate_total(), 50.00)

    def test_update_stock_rejects_negative(self):
        with self.assertRaises(ValueError):
            self.lamp.update_stock(-3)
        self.assertEqual(self.lamp.get_stock(), 10) # Stock is unchanged after the rejected update


if __name__ == "__main__":
    unittest.main()