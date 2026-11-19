from supplier import Supplier
from product_factory import ProductFactory
from order import Order

supplier = Supplier(1, "Tech Supplies Inc.", "techsupplies@example.com") # Create a Supplier object

print("\n--- Valid product: good data still works ---")
lamp = ProductFactory.create("physical", 1, "Desk Lamp", 25.00, 10, supplier, weight=1.2)
print(f"Created: {lamp.get_name()}, price ${lamp.get_price():.2f}, stock {lamp.get_stock()}")

print("\n--- Price of zero ---")
try:
    ProductFactory.create("physical", 2, "Free Lamp", 0, 10, supplier, weight=1.2)
except ValueError as error:
    print(f"Rejected: {error}")

print("\n--- Negative price ---")
try:
    ProductFactory.create("digital", 3, "Bad App", -5.00, 10, supplier, download_size=100)
except ValueError as error:
    print(f"Rejected: {error}")

print("\n--- Negative stock (physical) ---")
try:
    ProductFactory.create("physical", 4, "Chair", 49.90, -1, supplier, weight=8.0)
except ValueError as error:
    print(f"Rejected: {error}")

print("\n--- Negative stock (digital): LSP, the child cannot skip the parent's rule ---")
try:
    ProductFactory.create("digital", 5, "Photo Editor", 49.90, -1, supplier, download_size=500)
except ValueError as error:
    print(f"Rejected: {error}")

print("\n--- Order line quantity of zero ---")
order = Order(1)
try:
    order.add_order_line(lamp, 0)
except ValueError as error:
    print(f"Rejected: {error}")
print(f"Order lines after the rejected add: {len(order.get_order_lines())}") # Should still be 0, nothing half-added

print("\n--- Valid order line still works ---")
order.add_order_line(lamp, 2)
print(f"Order lines: {len(order.get_order_lines())}, total ${order.calculate_total():.2f}")