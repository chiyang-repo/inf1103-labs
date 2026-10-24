import json
import re
from datetime import datetime

from product import Product
from inventory import Inventory

def load_inventory():
    with open("inventory.json", 'r') as file: # Open the JSON file in read mode
        inventory_data = json.load(file) # Load the inventory data from the JSON file
        if len(inventory_data["products"]) == 0:  # Check if there are any products in the inventory
            print("\nNo products available in the inventory.")
            return inventory_data
        else:
            return inventory_data

        
def check_inventory_file_exists(): # Check if the inventory JSON file exists, and create it if it does not
    try:
        with open("inventory.json", 'r') as file: # Open the JSON file in read mode
            return True
    except FileNotFoundError: # If the inventory file does not exist, create a new one and return False
        with open("inventory.json", 'w') as file: # Open the JSON file in write mode
            json.dump({"products": []}, file) # Create a new inventory file with an empty list of products
            return False
        
def main():
    while True:
        inventory_exists = check_inventory_file_exists() # Check if the inventory JSON file exists, and create it if it does not
        if inventory_exists is True:
            inventory_message = "\ninventory.json found. \ninventory loaded successfully."
            inventory = load_inventory() # Load the inventory data from the JSON file
        else:
            inventory_message = "\ninventory.json not found. A new inventory file has been created."
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
5. Exit the program\n
Input your choice (1-5):""")
        match user_choice:
            case "1": load_inventory() # Call the load_inventory function to display the current inventory
            case "2": add_items() # Call the add_items function to add a new product to the inventory
            case "3": update_stock() # Call the update_items function to update an existing product in the inventory
            case "4": search_product() # Call the search_product function to search for a product in the inventory
            case "5":
                print("\nExiting the program.") # Exit the program
                break
            case _: print("Invalid choice. Please try again.\n") # Prompt the user to re-enter their choice if it is invalid
    
main()