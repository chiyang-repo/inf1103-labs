from abc import ABC, abstractmethod

class Product(ABC):
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def update_stock(self, new_stock):
        if not isinstance(new_stock, int) or new_stock < 0:
            raise ValueError("Stock must be a non-negative integer.")
        else:
            self.__stock = new_stock

    def display_information(self):
        print(f"Product ID: {self.__product_id}, Name: {self.__name}, Price: ${self.__price:.2f}, Stock: {self.__stock}")

    def to_dict(self): # Return the common product data as a dictionary, used when saving to JSON
        return {
            "product_id": self.__product_id,
            "product_name": self.__name,
            "quantity": self.__stock,
            "price": self.__price
        }
    @abstractmethod
    def get_fulfilment_info(self): 
        pass 


