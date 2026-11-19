import unittest
from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from product_factory import ProductFactory


class TestProductFactory(unittest.TestCase):
    def setUp(self) -> None: # Runs before every test
        self.supplier = Supplier(1, "Tech Supplies Inc.", "techsupplies@example.com")

    def test_creates_physical_product(self):
        guitar = ProductFactory.create("physical", 1, "Guitar", 299.90, 5, self.supplier, weight=3.5)
        self.assertIsInstance(guitar, PhysicalProduct)
        self.assertEqual(guitar.get_weight(), 3.5)

    def test_creates_digital_product(self):
        windows = ProductFactory.create("digital", 2, "Windows 11", 199.00, 50, self.supplier, download_size=5400)
        self.assertIsInstance(windows, DigitalProduct)
        self.assertEqual(windows.get_download_size(), 5400)

    def test_factory_returns_base_type_product(self): # The rest of the program only needs to know about Product
        for product_type in ["physical", "digital"]:
            with self.subTest(product_type=product_type):
                product = ProductFactory.create(product_type, 3, "Item", 10.00, 1, self.supplier)
                self.assertIsInstance(product, Product)

    def test_polymorphism_through_factory(self): # Same method call, each child gives its own answer
        guitar = ProductFactory.create("physical", 1, "Guitar", 299.90, 5, self.supplier, weight=3.5)
        windows = ProductFactory.create("digital", 2, "Windows 11", 199.00, 50, self.supplier, download_size=5400)
        self.assertIn("shipping", guitar.get_fulfilment_info())
        self.assertIn("download", windows.get_fulfilment_info())

    def test_messy_type_text_is_accepted(self):
        lamp = ProductFactory.create("  Physical ", 4, "Desk Lamp", 25.00, 10, self.supplier, weight=1.2)
        self.assertIsInstance(lamp, PhysicalProduct)

    def test_unknown_type_raises_clear_error(self): # Section 7: unknown type raises ValueError with a clear message
        with self.assertRaisesRegex(ValueError, "Unknown product type: service"):
            ProductFactory.create("service", 5, "Installation", 30.00, 5, self.supplier)

    def test_main_does_not_create_products_directly(self): # Section 7: products are created through the factory
        with open("main.py", encoding="utf-8") as file:
            source = file.read()
        self.assertNotIn("PhysicalProduct(", source)
        self.assertNotIn("DigitalProduct(", source)


if __name__ == "__main__":
    unittest.main()