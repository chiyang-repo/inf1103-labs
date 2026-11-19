from product import Product
from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())

supplier = Supplier(1, "Tech Supplies Inc.", "techsupplies@example.com") # Create a Supplier object

guitar = PhysicalProduct(1, "Guitar", 299.90, 5, 3.5, supplier) # Create a PhysicalProduct object
windows = DigitalProduct(2, "Windows 11", 199.00, 50, 5400, supplier) # Create a DigitalProduct object

print("\n--- physical product details ---")
show_product_details(guitar)
print("\n--- digital product details ---")
show_product_details(windows)

print("\n--- Normal Inventory operations on both types of products ---")
inventory_a = Inventory() # Create an Inventory object
inventory_a.add_product(guitar) # Add the PhysicalProduct to inventory_a
inventory_a.add_product(windows) # Add the DigitalProduct to inventory_a

inventory_a.display_all()
inventory_a.find_product(1).display_information() # Display the PhysicalProduct's information
inventory_a.search_product("guitar")[0].display_information() # Display the PhysicalProduct's information


print("\n--- Polymorphism: one loop over a mixed Inventory ---")
for product in inventory_a.get_products():
    show_product_details(product) # Display the product details for each product in the inventory