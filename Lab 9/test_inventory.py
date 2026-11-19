from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory


supplier = Supplier(1, "Tech Supplies Inc.", "techsupplies@example.com") # Create a Supplier object

guitar = PhysicalProduct(1, "Guitar", 299.90, 5, 3.5, supplier) # Create a PhysicalProduct object
windows = DigitalProduct(2, "Windows 11", 199.00, 50, 5400, supplier) # Create a DigitalProduct object

inventory_a = Inventory() # Create an Inventory object
inventory_b = Inventory() # Create another Inventory object

print("\n--- Before removing the guitar from inventory_a ---")
inventory_a.add_product(guitar) # Add the PhysicalProduct to inventory_a
inventory_a.display_all() # Display the PhysicalProduct's information

print("\n--- After removing the guitar from inventory_a ---")
inventory_a.remove_product(1) # Remove the PhysicalProduct from inventory_a
inventory_a.display_all() # Display the PhysicalProduct's information

print("\n--- Guitar used directly after removal from inventory_a ---")
guitar.display_information()

print("\n--- After adding the same guitar to inventory_b ---")
inventory_b.add_product(guitar) # Add the PhysicalProduct to inventory_b
inventory_b.display_all() # Display the PhysicalProduct's information

print(f"Same guitar object in inventory_b? {inventory_b.find_product(1) is guitar}")