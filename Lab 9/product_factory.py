from product import Product
from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct

# Create subclasses for physical and digital products
class ProductFactory:
    @staticmethod
    def create(product_type: str, product_id: int | str, name: str, price: float, stock: int, supplier: Supplier, weight: float = 0.0, download_size: float = 0.0) -> Product:
        product_type = product_type.strip().lower() 
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock, weight, supplier)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock, download_size, supplier)
        else:
            raise ValueError(f"Unknown product type: {product_type}")