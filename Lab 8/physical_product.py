from product import Product
from can_be_shipped import CanBeShipped
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    BASE_SHIPPING_FEE = 5.00 # Flat fee charged for every shipment
    SHIPPING_RATE_PER_KG = 2.00 # Extra cost for each kilogram of weight
    def __init__(self, product_id: int, name: str, price: float, stock: int, weight: float, supplier: Supplier) -> None: # Initialize the PhysicalProduct with the common attributes and the unique weight
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight: float = weight

    def get_weight(self) -> float: # Return the weight of the physical product
        return self.__weight

    def display_information(self) -> None:
        super().display_information()  # Display common product information
        self.get_supplier().display_information()  # Display supplier information
        print(f"Weight: {self.__weight}kg")  # Child adds the information unique to physical products


    def to_dict(self) -> dict: # Override: reuse Product's dictionary, then add the type and weight
        product_data = super().to_dict() # Parent builds the common fields
        product_data["type"] = "physical" # Type identifier used when loading the JSON back
        product_data["weight"] = self.__weight
        return product_data

    def get_fulfilment_info(self) -> str: # Implements Product's abstract method
        return "This product requires physical shipping to the customer."

    def calculate_shipping_cost(self) -> float: # Implements CanBeShipped's abstract method: shipping is based on weight
        return round(self.BASE_SHIPPING_FEE + self.__weight * self.SHIPPING_RATE_PER_KG, 2)
