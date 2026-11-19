import inspect
import unittest
from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from order import Order
from discount_strategy import NoDiscount, PercentageDiscount, BulkDiscount, StudentDiscount


class TestDiscountStrategy(unittest.TestCase):
    def setUp(self) -> None: # Runs before EVERY test, so each test starts with fresh objects
        supplier = Supplier(1, "Tech Supplies Inc.", "techsupplies@example.com")
        self.guitar = PhysicalProduct(1, "Guitar", 50.00, 10, 1.0, supplier) # 5 x 50 = 250
        self.windows = DigitalProduct(2, "Windows 11", 199.00, 50, 5400, supplier)

    def make_order(self, discount=None) -> Order: # Helper: an order totalling 250 with the given strategy
        order = Order(1, discount)
        order.add_order_line(self.guitar, 5)
        return order

    def test_no_strategy_defaults_to_no_discount(self):
        self.assertEqual(self.make_order().calculate_total(), 250.00)

    def test_no_discount_returns_total_unchanged(self):
        self.assertEqual(self.make_order(NoDiscount()).calculate_total(), 250.00)

    def test_bulk_discount_applies_at_or_above_threshold(self):
        self.assertEqual(self.make_order(BulkDiscount(200, 20)).calculate_total(), 230.00)

    def test_bulk_discount_not_applied_below_threshold(self):
        order = Order(3, BulkDiscount(200, 20))
        order.add_order_line(self.windows, 1) # 199 is below the 200 threshold
        self.assertEqual(order.calculate_total(), 199.00)

    def test_bulk_discount_never_goes_below_zero(self):
        self.assertEqual(BulkDiscount(10, 50).apply(20), 0)

    def test_percentage_discount(self):
        self.assertEqual(self.make_order(PercentageDiscount(10)).calculate_total(), 225.00)

    def test_set_discount_replaces_strategy(self): # Section 7: the strategy on an existing order can be changed
        order = self.make_order(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230.00)
        order.set_discount(PercentageDiscount(10))
        self.assertEqual(order.calculate_total(), 225.00) # Replaced, not stacked (stacked would be 207)

    def test_new_strategy_works_without_changing_order(self): # Section 7: a new strategy needs no change to Order
        self.assertEqual(self.make_order(StudentDiscount()).calculate_total(), 237.50)

    def test_one_strategy_shared_by_two_orders(self): # Evidence for the association relationship
        shared_discount = PercentageDiscount(10)
        order_5 = Order(5, shared_discount)
        order_5.add_order_line(self.guitar, 5)
        order_6 = Order(6, shared_discount)
        order_6.add_order_line(self.windows, 5)
        self.assertEqual(order_5.calculate_total(), 225.00)
        self.assertEqual(order_6.calculate_total(), 895.50)

    def test_order_has_no_discount_if_logic(self): # Section 7: Order contains no discount if/elif logic
        source = inspect.getsource(Order.calculate_total) # Reads the method's own source code as text
        self.assertNotIn("if ", source)
        self.assertNotIn("elif", source)

    def test_invalid_percentage_rejected(self):
        for bad in [0, -5, 150]:
            with self.subTest(percentage=bad): # Reports exactly which value failed, if one does
                with self.assertRaises(ValueError):
                    PercentageDiscount(bad)

    def test_invalid_bulk_values_rejected(self):
        with self.assertRaises(ValueError):
            BulkDiscount(0, 20)
        with self.assertRaises(ValueError):
            BulkDiscount(200, -5)


if __name__ == "__main__": # Lets you also run this one file directly
    unittest.main()