from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier

supplier = Supplier(1, "Tech Supplies Inc.", "techsupplies@example.com") # Create a Supplier object

guitar = PhysicalProduct(1, "Guitar", 299.90, 5, 3.5, supplier) # Create a PhysicalProduct object
windows = DigitalProduct(2, "Windows 11", 199.00, 50, 5400, supplier) # Create a DigitalProduct object


print(f"Same supplier object? {guitar.get_supplier() is windows.get_supplier()}")


print("\n--- Supplier accessed through guitar ---")
guitar.get_supplier().display_information() # Common product info + weight
windows.get_supplier().display_information() # Common product info + download size

del supplier # Removes the NAME 'supplier', not the Supplier object

print("\n--- After del supplier ---")
guitar.get_supplier().display_information()  # Still works: guitar holds a reference to the object
windows.get_supplier().display_information() # Still works: windows holds a reference too

try:
    supplier.display_information() # The name no longer exists, so this raises NameError
except NameError as error:
    print(f"Error: {error}. The name was removed, but the Supplier object still exists because the products reference it.")