import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
from supplier import Supplier
from inventory import Inventory
from main import get_positive_float, load_products


class TestUserInput(unittest.TestCase):
    def test_invalid_input_asks_again_then_returns_value(self): # Section 7: invalid input handled, user asked again
        output = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]), redirect_stdout(output): # Fake the 3 entries, capture prints
            value = get_positive_float("Enter the product price: ")
        self.assertEqual(value, 12.5)
        self.assertIsInstance(value, float)
        printed = output.getvalue()
        self.assertIn("Please enter a valid number, e.g. 12.50", printed) # From "abc" (exception handling)
        self.assertIn("Please enter a number greater than zero.", printed) # From "-5" (validation)

    def test_zero_is_rejected(self):
        with patch("builtins.input", side_effect=["0", "3"]), redirect_stdout(io.StringIO()):
            self.assertEqual(get_positive_float("Weight: "), 3.0)


class TestLoadProducts(unittest.TestCase):
    def setUp(self) -> None: # Runs before every test
        self.supplier = Supplier(1, "Tech Supplies Inc.", "techsupplies@example.com")
        self.inventory = Inventory()

    def load(self, path: str) -> str: # Helper: run load_products and return everything it printed
        output = io.StringIO()
        with redirect_stdout(output):
            load_products(path, self.inventory, self.supplier)
        return output.getvalue()

    def test_valid_rows_load(self): # Section 7: valid rows still load
        self.load("products.csv")
        self.assertEqual(len(self.inventory.get_products()), 3)
        for product_id in ["P001", "D001", "P003"]:
            with self.subTest(product_id=product_id):
                self.assertIsNotNone(self.inventory.find_product(product_id))

    def test_bad_rows_are_reported_and_skipped(self): # Section 7: bad rows reported and skipped
        printed = self.load("products.csv")
        self.assertIsNone(self.inventory.find_product("S001"))
        self.assertIsNone(self.inventory.find_product("P002"))
        self.assertIn("Unknown product type: service", printed)
        self.assertIn("could not convert string to float: 'abc'", printed)

    def test_message_order(self): # Matches the 5.2 prediction: skips, then count, then finally
        printed = self.load("products.csv")
        self.assertLess(printed.index("Skipped row 4"), printed.index("Skipped row 5"))
        self.assertLess(printed.index("Skipped row 5"), printed.index("3 products loaded."))
        self.assertLess(printed.index("3 products loaded."), printed.index("Load attempt finished."))

    def test_missing_file_is_handled(self): # Section 7: missing file handled gracefully (except + finally, no else)
        printed = self.load("missing.csv")
        self.assertIn("Products file not found: missing.csv", printed)
        self.assertIn("Load attempt finished.", printed)
        self.assertNotIn("products loaded", printed)
        self.assertEqual(len(self.inventory.get_products()), 0)


if __name__ == "__main__":
    unittest.main()