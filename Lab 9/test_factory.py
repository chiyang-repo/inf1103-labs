from product import Product
from supplier import Supplier
from product_factory import ProductFactory

supplier = Supplier(1, "Tech Supplies Inc.", "techsupplies@example.com") # Create a Supplier object

guitar = ProductFactory.create("physical", 1, "Guitar", 50.00, 10, supplier, weight=5) # Create a PhysicalProduct object
windows = ProductFactory.create("digital", 2, "Windows 11", 199.00, 50, supplier, download_size= 5400) # Create a DigitalProduct object

print("\n--- Polymorphism: each product shows its own child behaviour ---")
for product in [guitar, windows]:
    product.display_information()
    print(product.get_fulfilment_info())
    print(f"Is a Product? {isinstance(product, Product)}, actual class: {type(product).__name__}\n")

print("\n--- Unknown product type, caught with try/except ---")
try:
    ProductFactory.create("service", 4, "Installation", 30.00, 5, supplier)
except ValueError as error:
    print(f"Error caught: {error}")

print("\n--- Program carries on after the caught error ---")