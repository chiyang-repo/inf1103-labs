from product import Product

# Inventory class: manages a collection of Product objects (Single Responsibility Principle)
class Inventory:
    def __init__(self) -> None: # Initializer, starts with an empty inventory
        self.__products : list[Product] = []# Private list that stores the Product objects

    def add_product(self, product: Product) -> None: # Add a Product object to the inventory
        self.__products.append(product)

    def find_product(self, product_id: int) -> Product | None : # Return the Product with the matching ID, or None if there is no match
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def remove_product(self, product_id: int) -> Product | None: # Remove the Product with the matching ID from the inventory and return it, or return None if there is no match
        product_to_remove = self.find_product(product_id)
        if product_to_remove is not None:
            self.__products.remove(product_to_remove)
            return product_to_remove
        return None


    def search_product(self, name: str) -> list: # Return a list of Products whose name contains the search text (case-insensitive)
        return [product for product in self.__products if name.lower() in product.get_name().lower()]

    def display_all(self) -> None: # Print every product in the inventory
        if len(self.__products) == 0: # Check if there are any products in the inventory
            print("\nNo products available in the inventory.")
            return
        print("\nCurrent Inventory: \n---------------------------------------------------------------")
        for product in self.__products:
            product.display_information() # Each Product displays its own information
        print("---------------------------------------------------------------")

    def get_products(self) -> list[Product]: # Return a copy of the product list, so outside code cannot change the inventory's own list
        return list(self.__products)

    
        
        