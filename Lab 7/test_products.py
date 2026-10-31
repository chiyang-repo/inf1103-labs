from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct

guitar = PhysicalProduct(1, "Guitar", 299.90, 5, 3.5) # Create a PhysicalProduct object
guitar.display_information() # Common product info + weight

windows = DigitalProduct(2, "Windows 11", 199.00, 50, 5400) # Create a DigitalProduct object
windows.display_information() # Common product info + download size

print(guitar.get_fulfilment_info()) # PhysicalProduct's version
print(windows.get_fulfilment_info()) # DigitalProduct's version

try:
    generic = Product(3, "Generic Item", 10.00, 1) # Should fail: Product is abstract
except TypeError as error:
    print(f"Cannot create a Product directly: {error}")