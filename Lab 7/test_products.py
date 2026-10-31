from physical_product import PhysicalProduct
from digital_product import DigitalProduct

guitar = PhysicalProduct(1, "Guitar", 299.90, 5, 3.5) # Create a PhysicalProduct object
guitar.display_information() # Common product info + weight

windows = DigitalProduct(2, "Windows 11", 199.00, 50, 5400) # Create a DigitalProduct object
windows.display_information() # Common product info + download size