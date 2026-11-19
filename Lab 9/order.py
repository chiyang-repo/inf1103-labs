from product import Product
from order_line import OrderLine

class Order:
    def __init__(self, order_id: int) -> None: # Initialize the Order with an ID and a list of OrderLine objects
        self.__order_id: int = order_id
        self.__order_lines: list[OrderLine] = []

    def get_order_lines(self) -> list[OrderLine]: # Return a copy of the order lines, so outside code cannot change the order's own list
            return list(self.__order_lines)

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def calculate_total(self) -> float: # Calculate the total cost of the order by summing the subtotals of each order line
        total = 0.0
        for order_line in self.__order_lines:
            total += order_line.calculate_subtotal()
        return total

    def remove_order_line(self, product_id: int) -> None:  # Remove the order line for the product with this ID; the Order manages its own lines
        for order_line in self.__order_lines:
            if order_line.get_product().get_product_id() == product_id:
                self.__order_lines.remove(order_line)
                break

    def display_order(self) -> None: # Display the order ID, each order line's information, and the total cost
        print(f"Order ID: {self.__order_id}")
        for order_line in self.__order_lines:
            order_line.display_information()
        print(f"Total Order Cost: ${self.calculate_total():.2f}")


    