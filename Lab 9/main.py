import json
import re
import csv
from datetime import datetime

from product_factory import ProductFactory
from supplier import Supplier
from inventory import Inventory

def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None: # Load products from a CSV file through the ProductFactory, skipping bad rows
    try:
        file = open(path, newline="") # Only the open() is in the try, so we know FileNotFoundError came from here
    except FileNotFoundError: # The file does not exist: report it simply instead of crashing
        print(f"Products file not found: {path}")
    else: # Only runs if the file opened successfully
        loaded = 0
        with file: # Makes sure the file is closed when we are done
            reader = csv.reader(file)
            next(reader, None) # Skip the header row
            for row_number, row in enumerate(reader, start=2): # start=2 because line 1 is the header
                try: # Each row has its own try, so one bad row does not stop the rest
                    product_type, product_id, name, price, stock = row # A row with the wrong number of columns also raises ValueError
                    product = ProductFactory.create(product_type, product_id, name, float(price), int(stock), supplier)
                except ValueError as error: # Unknown type, a price/stock that is not a number, or failed validation
                    print(f"Skipped row {row_number} {row}: {error}")
                    continue
                inventory.add_product(product)
                loaded += 1
        print(f"{loaded} products loaded.")
    finally: # Always runs, whether the file was found or not
        print("Load attempt finished.")

def transactional_history(action: str, product_name: str, product_quantity: int, product_price: float, supplier: Supplier) -> None: # Log the product addition or update to the transactional history file
    with open("inventory.txt", 'a') as file:
        file.write(f"[{datetime.now()}] {action}: {product_name}, Quantity: {product_quantity}, Price: {product_price}, Supplier: {supplier.get_name()}\n")


def validate_product_entry(product_name: str, product_quantity: str) -> bool: # Validate that the name and quantity are filled in and the quantity is a non-negative whole number
    if not product_name or not product_quantity: # Check if any of the fields are empty
        print("\nAll fields are required. Please provide valid inputs.")
        return False
    elif not product_quantity.isdigit() or int(product_quantity) < 0: # Check if product quantity is a non-negative integer
        print("\nInvalid quantity. Please enter a non-negative integer.")
        return False
    return True

def choose_product_type() -> str: # Ask the user whether the new product is physical or digital, and return "physical" or "digital"
    while True:
        product_type = input("Is this a (1) Physical or (2) Digital product? Enter 1 or 2: ")
        if product_type == "1":
            return "physical"
        elif product_type == "2":
            return "digital"
        print("Invalid choice. Please enter 1 or 2.") # Keep asking until a valid choice is entered

def get_positive_float(prompt: str) -> float: # Keep asking until the user enters a number greater than 0 (used for price, weight and download size)
    while True:
        try:
            value = float(input(prompt)) # float() raises ValueError for text like "abc"
            if value <= 0: # Validation: the conversion worked but the number breaks the rule
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError: # Exception handling: only catch the error we expect, not every error
            print("Please enter a valid number, e.g. 12.50")

def choose_supplier(suppliers: dict[int, Supplier]) -> Supplier: # Ask the user to choose a supplier from the list of suppliers, and return the selected Supplier object
    print("\nAvailable Suppliers:")
    for supplier_id, supplier in suppliers.items():
        print(f"{supplier_id}. {supplier.get_name()} ({supplier.get_contact_email()})")
    while True:
        supplier_choice = input("Enter the supplier ID for this product: ")
        if supplier_choice.isdigit() and int(supplier_choice) in suppliers:
            return suppliers[int(supplier_choice)]
        else:
            print("Invalid choice. Please enter a valid supplier ID.")

def add_product(inventory: Inventory, suppliers: dict[int, Supplier]) -> None: # Ask the user for a new product's details and add it to the inventory
    if len(suppliers) == 0:
        print("No suppliers available. Please add a supplier first.")
        return
    product_type = choose_product_type() # Physical or digital decides which extra detail to ask for and which class to create
    chosen_supplier = choose_supplier(suppliers) # Ask the user to choose a supplier from the list of suppliers
    while True:
        product_name = input("Enter the product name: ") # Prompt the user to enter the product name
        product_quantity = input("Enter the product quantity: ") # Prompt the user to enter the product quantity
        if validate_product_entry(product_name, product_quantity) is True: # Validate the name and quantity
            break
        print("Invalid product entry. Please try again.") # Prompt the user to re-enter the product details if the entry is invalid

    price = get_positive_float("Enter the product price: ") # Keeps asking until the price is a number greater than 0
    product_id = len(inventory.get_products()) + 1 # Get the next product ID based on the number of existing products
    quantity = int(product_quantity)
    weight = 0.0 # Only one of these two will be filled in, depending on the type
    download_size = 0.0
    if product_type == "physical": # This if only decides which question to ask, not which class to create
        weight = get_positive_float("Enter the product weight (kg): ") # Extra detail only physical products have
    else:
        download_size = get_positive_float("Enter the download size (MB): ") # Extra detail only digital products have
    product = ProductFactory.create(product_type, product_id, product_name, price, quantity, chosen_supplier, weight=weight, download_size=download_size) # The factory creates the correct subclass
    inventory.add_product(product) # Store it in the inventory (in memory, saved later)
    print("Product added successfully.")
    transactional_history(f"ADDED ({product_type})", product_name, quantity, price, chosen_supplier) # Log the addition, including its type

def add_supplier(suppliers: dict[int, Supplier]) -> None: # Ask the user for a new supplier's details and add it to the suppliers dictionary
    while True:
        supplier_name = input("Enter the supplier name: ") # Prompt the user to enter the supplier name
        contact_email = input("Enter the supplier contact email: ") # Prompt the user to enter the supplier contact email
        if not supplier_name or not contact_email: # Check if any of the fields are empty
            print("\nAll fields are required. Please provide valid inputs.")
            continue
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", contact_email): # Check if the email format is valid
            print("\nInvalid email format. Please enter a valid email address.")
            continue
        break

    supplier_id = max(suppliers, default=0) + 1 # Get the next supplier ID based on the number of existing suppliers
    new_supplier = Supplier(supplier_id, supplier_name, contact_email) # Create a Supplier object
    suppliers[supplier_id] = new_supplier # Store it in the suppliers dictionary
    print("Supplier added successfully.")

def update_stock(inventory: Inventory) -> None: # Ask the user which product to update and its new stock quantity
    products = inventory.get_products() # Get a copy of the product list to check for valid IDs
    if len(products) == 0: # Check if there are any products in the inventory
        print("No products available to update.")
        return
    else:
        inventory.display_all()
        while True:
            product_id = input("Enter the product ID to update: ") # Prompt the user to enter the product ID of the product they want to update
            try:
                product_id = int(product_id) # Check the input is an integer
            except ValueError:
                print("Invalid product ID. Please enter a whole number.")
                continue
            if product_id < 0: # Check the ID is not negative
                print("Invalid product ID. The ID cannot be negative.")
                continue
            elif product_id < 1 or product_id > len(products): # Check the ID is within the range of products in the inventory
                print(f"Invalid product ID. Please enter an ID between 1 and {len(products)}.")
                continue
            else:
                product = inventory.find_product(product_id) # Get the Product object with that ID
                if product is None: # Safety net in case an ID inside the range does not exist
                    print("Invalid product ID. Please try again.")
                    continue
                break
        while True:
            product_quantity = input("Enter the new product quantity: ") # Prompt the user to enter the new product quantity
            try:
                product.update_stock(int(product_quantity)) # int() raises ValueError for non-numbers, Product raises it for negative numbers
                break
            except ValueError:
                print("Invalid stock entry. Please enter a non-negative whole number.")
        print("\nStock updated successfully.")
        transactional_history("UPDATED", product.get_name(), product.get_stock(), product.get_price(), product.get_supplier()) # Log the product update to the transactional history

def search_product(inventory: Inventory) -> None: # Ask the user for a name and display the matching products
    if len(inventory.get_products()) == 0: # Check if there are any products in the inventory
        print("No products available to search.")
        return
    product_name = input("Enter the product name to search: ") # Prompt the user to enter the product name they want to search for
    found_products = inventory.search_product(product_name) # Inventory does the searching and returns the matches
    if len(found_products) > 0: # Check if any products were found
        print("\nSearch Results:")
        for product in found_products:
            product.display_information()
    else:
        print("\nNo products found matching the search criteria.")

def save_inventory(inventory: Inventory, suppliers: dict[int, Supplier]) -> None: # Write every Product back to inventory.json in one go
    suppliers_data = {"suppliers": []}
    inventory_data = {"products": []}
    for supplier in suppliers.values(): # Each Supplier turns itself into a dictionary
        suppliers_data["suppliers"].append(supplier.to_dict())
    for product in inventory.get_products(): # Each product turns itself into a dictionary, including its type
        inventory_data["products"].append(product.to_dict())

    with open("inventory.json", 'w') as file: # 'w' replaces the whole file with the current inventory
        json.dump({"suppliers": suppliers_data["suppliers"], "products": inventory_data["products"]}, file, indent=4)

def main() -> None: # Main program loop, handles the menu and user choices
    inventory = Inventory() # Create the one Inventory object the whole program shares
    suppliers : dict[int, Supplier] = {}
    if load_products(inventory, suppliers): # Read inventory.json ONCE, before the menu loop
        inventory_message = "\ninventory.json found. \ninventory loaded successfully."
    else:
        inventory_message = "\ninventory.json not found. Starting with an empty inventory."
    while True:
        user_choice = input(f"""
==============================================
Inventory Management System
==============================================
{inventory_message}
\n 
1. Display current inventory
2. Add product 
3. Add supplier
4. Update stock
5. Search product
6. Save inventory
7. Exit the program\n
Input your choice (1-7):""")
        match user_choice:
            case "1": inventory.display_all() # Display the current inventory from memory
            case "2": add_product(inventory, suppliers) # Call the add_product function to add a new product to the inventory
            case "3": add_supplier(suppliers) # Call the add_supplier function to add a new supplier to the suppliers dictionary
            case "4": update_stock(inventory) # Call the update_stock function to update an existing product in the inventory
            case "5": search_product(inventory) # Call the search_product function to search for a product in the inventory
            case "6":
                save_inventory(inventory, suppliers) # Write the inventory to inventory.json
                print("\nInventory saved.")
            case "7":
                save_inventory(inventory, suppliers) # Save all changes before exiting
                print("\nInventory saved. Exiting the program.")
                break
            case _: print("Invalid choice. Please try again.\n") # Prompt the user to re-enter their choice if it is invalid


if __name__ == "__main__": 
    main()