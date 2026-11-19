from supplier import Supplier
from inventory import Inventory
from main import load_products

supplier = Supplier(1, "Tech Supplies Inc.", "techsupplies@example.com") # Create a Supplier object

print("\n--- Loading products.csv (bad rows should be skipped) ---")
inventory = Inventory()
load_products("products.csv", inventory, supplier)
inventory.display_all()

print("\n--- Products loaded by ID ---")
for product_id in ["P001", "D001", "S001", "P002", "P003"]:
    print(f"{product_id}: {'loaded' if inventory.find_product(product_id) else 'not loaded'}")

print("\n--- Loading a file that does not exist ---")
empty_inventory = Inventory()
load_products("missing.csv", empty_inventory, supplier)
print(f"Products in inventory: {len(empty_inventory.get_products())}")

print("\n--- Program carries on after both loads ---")