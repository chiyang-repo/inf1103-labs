import json
import re
from datetime import datetime

from product import Product
from inventory import Inventory

def load_inventory(inventory): # Read inventory.json once and fill the Inventory with Product objects
    try:
        with open("inventory.json", 'r') as file: # Open the JSON file in read mode
            inventory_data = json.load(file) # Load the raw dictionary data from the JSON file
            for item in inventory_data["products"]: # Each item is a dictionary from the JSON file
                product = Product(item["product_id"], item["product_name"], item["price"], item["quantity"]) # Turn the dictionary into a Product object
                inventory.add_product(product) # add_product() puts it into Inventory's private list
            return True
    except FileNotFoundError: # The file does not exist, so leave the inventory empty
        return False

def transactional_history(action, product_name, product_quantity, product_price): # Log the product addition or update to the transactional history file
    with open("inventory.txt", 'a') as file:
        file.write(f"[{datetime.now()}] {action}: {product_name}, Quantity: {product_quantity}, Price: {product_price}\n")


def validate_product_entry(product_name, product_quantity, product_price): # Validate the product entry to ensure that all fields are filled and that the quantity and price are valid
    if not product_name or not product_quantity or not product_price: # Check if any of the fields are empty
        print("\nAll fields are required. Please provide valid inputs.")
        return False
    elif not product_quantity.isdigit() or int(product_quantity) < 0: # Check if product quantity is a non-negative integer or a string
        print("\nInvalid quantity. Please enter a non-negative integer.")
        return False
    elif not re.match(r"^\d+(\.\d+)?$", product_price): # Check if product price is valid price format (non-negative number with optional decimal)
        print("\nInvalid price. Please enter a non-negative number.")
        return False
    return True

def add_product(inventory): # Ask the user for a new product's details and add it to the inventory
    while True:
        product_name = input("Enter the product name: ") # Prompt the user to enter the product name
        product_quantity = input("Enter the product quantity: ") # Prompt the user to enter the product quantity
        product_price = input("Enter the product price: ") # Prompt the user to enter the product price
        if validate_product_entry(product_name, product_quantity, product_price) is True: # Validate the product entry
            product_id = len(inventory.get_products()) + 1 # Get the next product ID based on the number of existing products
            product = Product(product_id, product_name, round(float(product_price), 2), int(product_quantity)) # Create the new Product object
            inventory.add_product(product) # Store it in the inventory (in memory, saved later)
            print("Product added successfully.")
            transactional_history("ADDED", product_name, product_quantity, product_price) # Log the product addition to the transactional history
            break
        else:
            print("Invalid product entry. Please try again.") # Prompt the user to re-enter the product details if the entry is invalid

def update_stock(inventory): # Ask the user which product to update and its new stock quantity
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
                product = inventory.find_by_id(product_id) # Get the Product object with that ID
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
        transactional_history("UPDATED", product.get_name(), product_quantity, product.get_price()) # Log the product update to the transactional history

def search_product(inventory): # Ask the user for a name and display the matching products
    if len(inventory.get_products()) == 0: # Check if there are any products in the inventory
        print("No products available to search.")
        return
    product_name = input("Enter the product name to search: ") # Prompt the user to enter the product name they want to search for
    found_products = inventory.search_product(product_name) # Inventory does the searching and returns the matches
    if len(found_products) > 0: # Check if any products were found
        print("\nSearch Results:")
        for product in found_products:
            product.display_product()
    else:
        print("\nNo products found matching the search criteria.")

def save_inventory(inventory): # Write every Product back to inventory.json in one go
    inventory_data = {"products": []}
    for product in inventory.get_products(): # Turn each Product object back into a dictionary
        inventory_data["products"].append({
            "product_id": product.get_product_id(),
            "product_name": product.get_name(),
            "quantity": product.get_stock(),
            "price": product.get_price()
        })
    with open("inventory.json", 'w') as file: # 'w' replaces the whole file with the current inventory
        json.dump(inventory_data, file, indent=4)

def main():
    inventory = Inventory() # Create the one Inventory object the whole program shares
    if load_inventory(inventory): # Read inventory.json ONCE, before the menu loop
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
3. Update stock
4. Search product
5. Save inventory
6. Exit the program\n
Input your choice (1-6):""")
        match user_choice:
            case "1": inventory.display_all() # Display the current inventory from memory
            case "2": add_product(inventory) # Call the add_product function to add a new product to the inventory
            case "3": update_stock(inventory) # Call the update_stock function to update an existing product in the inventory
            case "4": search_product(inventory) # Call the search_product function to search for a product in the inventory
            case "5":
                save_inventory(inventory) # Write the inventory to inventory.json
                print("\nInventory saved.")
            case "6":
                save_inventory(inventory) # Save all changes before exiting
                print("\nInventory saved. Exiting the program.")
                break
            case _: print("Invalid choice. Please try again.\n") # Prompt the user to re-enter their choice if it is invalid
main()