from abc import ABC, abstractmethod
from supplier import Supplier

class Product(ABC):
    def __init__(self, product_id: int, name: str, price: float, stock: int, supplier: Supplier) -> None: # Initialize the Product with the common attributes and a Supplier object
        self.__product_id: int = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.__supplier: Supplier = supplier

    def get_product_id(self) -> int:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def update_stock(self, new_stock: int) -> None: # Update the stock quantity, ensuring it is a non-negative integer
        if not isinstance(new_stock, int) or new_stock < 0:
            raise ValueError("Stock must be a non-negative integer.")
        else:
            self.__stock = new_stock

    def display_information(self) -> None: # Print the common product information
        print(f"Product ID: {self.__product_id}, Name: {self.__name}, Price: ${self.__price:.2f}, Stock: {self.__stock}")

    def to_dict(self) -> dict: # Return the common product data as a dictionary, used when saving to JSON
        return {
            "product_id": self.__product_id,
            "product_name": self.__name,
            "quantity": self.__stock,
            "price": self.__price
        }
    @abstractmethod
    def get_fulfilment_info(self) -> str: # Abstract method to be implemented by subclasses, providing information on how the product is fulfilled
        pass 


