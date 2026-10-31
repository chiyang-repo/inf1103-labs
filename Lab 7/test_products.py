from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped

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


light_item = PhysicalProduct(4, "Phone Case", 15.00, 100, 0.5) # Physical products of different weights
heavy_item = PhysicalProduct(5, "Amplifier", 450.00, 3, 20)

print(f"{light_item.get_name()} (0.5kg) shipping cost: ${light_item.calculate_shipping_cost():.2f}")
print(f"{guitar.get_name()} (3.5kg) shipping cost: ${guitar.calculate_shipping_cost():.2f}")
print(f"{heavy_item.get_name()} (20kg) shipping cost: ${heavy_item.calculate_shipping_cost():.2f}")

print(f"Can the guitar be shipped? {isinstance(guitar, CanBeShipped)}") # True: PhysicalProduct implements the interface
print(f"Can Windows 11 be shipped? {isinstance(windows, CanBeShipped)}") # False: DigitalProduct does not