class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def get_product_id(self):
        return self.product_id

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def get_stock(self):
        return self.stock

    def update_stock(self, new_stock):
        if not isinstance(new_stock, int) or new_stock < 0:
            raise ValueError("Stock must be a non-negative integer.")
        else:
            self.stock = new_stock

    def display_product(self):
        return f"Product ID: {self.product_id}, Name: {self.name}, Price: ${self.price:.2f}, Stock: {self.stock}"

product1 = Product("P001", "Product 1", 10.99, 100)
print(product1.display_product())
