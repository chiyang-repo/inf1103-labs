from order import Order
from discount_strategy import BulkDiscount, PercentageDiscount, StudentDiscount
from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct

supplier = Supplier(1, "Tech Supplies Inc.", "techsupplies@example.com") # Create a Supplier object

guitar = PhysicalProduct(1, "Guitar", 50.00, 10, 1.0, supplier) # Create a PhysicalProduct object
windows = DigitalProduct(2, "Windows 11", 199.00, 50, 5400, supplier) # Create a DigitalProduct object

print("\n--- No strategy given (should default to NoDiscount) ---")
order_1 = Order(1)
order_1.add_order_line(guitar, 5)
print(f"Total: ${order_1.calculate_total():.2f}")

print("\n--- Bulk Discount ---")
order_2 = Order(2, BulkDiscount(200,20))
order_2.add_order_line(guitar, 5)
print(f"Total: ${order_2.calculate_total():.2f}")

print("\n--- Same order after set_discount(PercentageDiscount(10)) ---")
order_2.set_discount(PercentageDiscount(10))
print(f"Total: ${order_2.calculate_total():.2f}")

print("\n--- BulkDiscount(200, 20) on an order below the threshold ---")
order_3 = Order(3, BulkDiscount(200, 20))
order_3.add_order_line(windows, 1) 
print(f"Total: ${order_3.calculate_total():.2f}")

print("\n--- display_order() should show the discounted total ---")
order_2.display_order()

print("\n--- Student Discount ---")
order_4 = Order(4)
order_4.add_order_line(guitar, 5)
order_4.set_discount(StudentDiscount())
print(f"Total: ${order_4.calculate_total():.2f}")

print("\n--- Shared Discount ---")
order_5 = Order(5)
order_6 = Order(6)
order_5.add_order_line(guitar, 5)
order_6.add_order_line(windows, 5)

shared_discount = PercentageDiscount(10)
order_5.set_discount(shared_discount)
order_6.set_discount(shared_discount)
print(f"Order_5 Total: ${order_5.calculate_total():.2f}")
print(f"Order_6 Total: ${order_6.calculate_total():.2f}")
