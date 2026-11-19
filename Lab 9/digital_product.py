from product import Product
from supplier import Supplier

class DigitalProduct(Product):
    def __init__(self, product_id: int, name: str, price: float, stock: int, download_size: float, supplier: Supplier) -> None: # Initialize the DigitalProduct with the common attributes and the unique download size
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size: float = download_size

    def get_download_size(self) -> float: # Return the download size of the digital product
        return self.__download_size

    def display_information(self) -> None:
        super().display_information()  # Display common product information
        self.get_supplier().display_information()  # Display supplier information
        print(f"Download Size: {self.__download_size}MB")  # Child adds the information unique to digital products

    def to_dict(self) -> dict: # Override: reuse Product's dictionary, then add the type and weight
        product_data = super().to_dict() # Parent builds the common fields
        product_data["type"] = "digital" # Type identifier used when loading the JSON back
        product_data["download_size"] = self.__download_size
        return product_data

    def get_fulfilment_info(self) -> str: # Implements Product's abstract method
        return "This product is delivered digitally via a download link."
    