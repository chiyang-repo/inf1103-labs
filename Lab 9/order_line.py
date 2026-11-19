from product import Product

class OrderLine:
    def __init__(self, product: Product, quantity: int) -> None: # Initialize the OrderLine with a Product object and the quantity ordered
        self.__product: Product = product
        if not isinstance(quantity, int) or quantity < 1: # Validate that the quantity is a positive integer
            raise ValueError("Quantity must be a positive integer.")
        else:
            self.__quantity: int = quantity

    def get_product(self) -> Product: # Public method to access the Product object associated with this order line
        return self.__product

    def get_quantity(self) -> int: # Public method to access the quantity ordered for this order line
        return self.__quantity

    def calculate_subtotal(self) -> float: # Calculate the subtotal for this order line (product price multiplied by quantity)
        return self.__product.get_price() * self.__quantity

    def display_information(self) -> None: # Display the order line information, including product details and subtotal
        self.__product.display_information()  # Display the product information
        print(f"Quantity: {self.__quantity}, Subtotal: ${self.calculate_subtotal():.2f}")  # Display the quantity and subtotal

    
