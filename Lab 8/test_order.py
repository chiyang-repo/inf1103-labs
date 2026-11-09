from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from order import Order


supplier = Supplier(1, "Tech Supplies Inc.", "techsupplies@example.com") # Create a Supplier object

guitar = PhysicalProduct(1, "Guitar", 299.90, 5, 3.5, supplier) # Create a PhysicalProduct object
windows = DigitalProduct(2, "Windows 11", 199.00, 50, 5400, supplier) # Create a DigitalProduct objects


order_1 = Order(1)
order_1.add_order_line(guitar, 2) # Add 2 guitars to the order
order_1.add_order_line(windows, 1) # Add 1 Windows 11 to the order
order_1.display_order() # Display the order details, including the total cost and shipping cost
order_1.get_order_lines()[0].get_product().display_information()
order_1.get_order_lines()[1].get_product().display_information()



order_2 = Order(2)
order_2.add_order_line(guitar, 1) # Add 1 guitar to the order
order_2.display_order() # Display the order details, including the total cost and shipping cost

print(f"Same Product object? {order_1.get_order_lines()[0].get_product() is order_2.get_order_lines()[0].get_product()}")
print(f"Same OrderLine object? {order_1.get_order_lines()[0] is order_2.get_order_lines()[0]}")