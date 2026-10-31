from product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    BASE_SHIPPING_FEE = 5.00 # Flat fee charged for every shipment
    SHIPPING_RATE_PER_KG = 2.00 # Extra cost for each kilogram of weight
    def __init__(self, product_id, name, price, stock, weight): # Initialize the PhysicalProduct with the common attributes and the unique weight
        super().__init__(product_id, name, price, stock)
        self.__weight = weight

    def get_weight(self): # Return the weight of the physical product
        return self.__weight

    def display_information(self):
        super().display_information()  # Display common product information
        print(f"Weight: {self.__weight}kg")  # Child adds the information unique to physical products  

    def get_fulfilment_info(self): # Implements Product's abstract method
        return "This product requires physical shipping to the customer."

    def calculate_shipping_cost(self): # Implements CanBeShipped's abstract method: shipping is based on weight
        return round(self.BASE_SHIPPING_FEE + self.__weight * self.SHIPPING_RATE_PER_KG, 2)
