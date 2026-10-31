from product import Product

class PhysicalProduct(Product):
    def __init__(self, product_id, name, price, stock, weight): # Initialize the PhysicalProduct with the common attributes and the unique weight
        super().__init__(product_id, name, price, stock)
        self.__weight = weight

    def get_weight(self): # Return the weight of the physical product
        return self.__weight

    def display_information(self):
        super().display_information()  # Display common product information
        print(f"Weight: {self.__weight}kg")  # Child adds the information unique to physical products  
