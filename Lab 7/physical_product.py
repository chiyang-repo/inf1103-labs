from product import Product

class PhysicalProduct(Product):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight

    def get_weight(self):
        return self.__weight

    def display_information(self):
        print(f"Product ID: {self.get_product_id()}, Name: {self.get_name()}, Price: ${self.get_price():.2f}, Stock: {self.get_stock()}, Weight: {self.__weight}kg")

