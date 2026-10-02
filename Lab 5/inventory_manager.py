# Package imports
import json
import re
from datetime import datetime


def check_inventory_file_exists(): # Check if the inventory JSON file exists, and create it if it does not
    try:
        with open("inventory.json", 'r') as file: # Open the JSON file in read mode
            return True
    except FileNotFoundError: # If the inventory file does not exist, create a new one and return False
        with open("inventory.json", 'w') as file: # Open the JSON file in write mode
            json.dump({"products": []}, file) # Create a new inventory file with an empty list of products
            return False

# Function to load inventory from JSON file
def load_inventory():
    with open("inventory.json", 'r') as file: # Open the JSON file in read mode
        inventory_data = json.load(file) # Load the inventory data from the JSON file
        if len(inventory_data["products"]) == 0:  # Check if there are any products in the inventory
            print("\nNo products available in the inventory.")
            return
        else:
            print("\nCurrent Inventory: \n---------------------------------------------------------------")
            for product in inventory_data["products"]:  # Iterate through the inventory data and print each product
                product_id =  product["product_id"]
                product_name = product["product_name"]
                product_quantity = product["quantity"]
                product_price = product["price"]
                print(f"ID: {product_id} | Name: {product_name} | Price: {product_price} | Quantity: {product_quantity}")
            print("---------------------------------------------------------------")

def add_items(): # Add new products to the inventory
    with open("inventory.json", 'r') as file: # Open the JSON file in read mode to get the current product ID
        inventory_data = json.load(file)
        product_id = len(inventory_data["products"])  # Get the next product ID based on the number of existing products
    with open("inventory.json", 'w') as file: # Open the JSON file in write mode to add new products
        while True:
            product_name = input("Enter the product name: ") # Prompt the user to enter the product name
            product_quantity = input("Enter the product quantity: ") # Prompt the user to enter the product quantity
            product_price = input("Enter the product price: ") # Prompt the user to enter the product price
            valid_product = validate_product_entry(product_name,product_quantity,product_price) # Validate the product entry
            if valid_product is True:
                # Write the product data to the JSON file
                new_product = {
                    "product_id": int(product_id) + 1,
                    "product_name": product_name,
                    "quantity": int(product_quantity),
                    "price": round(float(product_price), 2)
                }
                inventory_data["products"].append(new_product)
                json.dump(inventory_data, file)
                print("Product added successfully.")
                transactional_history("ADDED", product_name, product_quantity, product_price) # Log the product addition to the transactional history
                break
            else:
                print("Invalid product entry. Please try again.") # Prompt the user to re-enter the product details if the entry is invalid
                
def update_stock(): # Update the stock quantity of existing products in the inventory
    with open("inventory.json", 'r') as file: # Open the JSON file in read mode to get the current inventory data
        inventory_data = json.load(file)
        if len(inventory_data["products"]) == 0:  # Check if there are any products in the inventory
            print("No products available to update.")
            return
        print("\nCurrent Inventory:")
        for product in inventory_data["products"]:
            print(f"{product['product_id']} | {product['product_name']} | {product['quantity']} | {product['price']}")
        while True:
            product_id = input("Enter the product ID to update: ") # Prompt the user to enter the product ID of the product they want to update
            if not product_id.isdigit() or int(product_id) < 1 or int(product_id) > len(inventory_data["products"]):
                print("Invalid product ID. Please try again.")
                continue
            else:
                product_quantity = input("Enter the new product quantity: ") # Prompt the user to enter the new product quantity
                if not product_quantity.isdigit() or int(product_quantity) < 0: # Check if the new product quantity is a non-negative integer
                    print("Invalid stock entry. Please try again.")
                    continue
                # Update the product data in the JSON file
                else:
                    inventory_data["products"][int(product_id) - 1]["quantity"] = int(product_quantity)
                    with open("inventory.json", 'w') as file: # Open the JSON file in write mode to update the product data
                        json.dump(inventory_data, file)
                        print("\nStock updated successfully.")
                        transactional_history("UPDATED", inventory_data["products"][int(product_id) - 1]["product_name"], product_quantity, inventory_data["products"][int(product_id) - 1]["price"]) # Log the product update to the transactional history
                        break

def transactional_history(action, product_name, product_quantity, product_price): # Log the product addition or update to the transactional history file
    with open("inventory.txt", 'a') as file:
        file.write(f"[{datetime.now()}] {action}: {product_name}, Quantity: {product_quantity}, Price: {product_price}\n")
    return


def save_inventory(product_quantity, order_quantity, product_id): # Update the inventory after an order is placed
    with open("inventory.csv", 'r', newline='') as file: # Open the CSV file in read mode to get the current inventory data
        reader = csv.reader(file)
        inventory_data = list(reader)
        updated_product_quantity = int(product_quantity) - int(order_quantity) # Calculate the updated product quantity after the order is placed
        if updated_product_quantity == 0:
            inventory_data.pop(int(product_id))  # Remove the product from the inventory if quantity is zero
            for row in range(1, len(inventory_data)):  # Update the product IDs for the remaining products
                inventory_data[row][0] = str(row)
            with open("inventory.csv", 'w', newline='') as file: # Open the CSV file in write mode to update the inventory data
                writer = csv.writer(file)
                writer.writerows(inventory_data)
                print("\nInventory updated successfully.")
        else:
            inventory_data[int(product_id)][2] = str(updated_product_quantity)  # Update the product quantity in the inventory
            with open("inventory.csv", 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(inventory_data)
            print("\nInventory updated successfully.")


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

def search_product(): # Search for a product in the inventory by name
    with open("inventory.json", 'r') as file: # Open the JSON file in read mode to get the current inventory data
        inventory_data = json.load(file)
        if len(inventory_data["products"]) == 0:  # Check if there are any products in the inventory
            print("No products available to search.")
            return
        product_name = input("Enter the product name to search: ") # Prompt the user to enter the product name they want to search for
        found_products = [product for product in inventory_data["products"] if product_name.lower() in product["product_name"].lower()] # Search for products that match the entered name (case-insensitive)
        if found_products:
            print("\nSearch Results:")
            for product in found_products:
                print(f"ID: {product['product_id']} \nName: {product['product_name']} \nPrice: {product['price']} \nQuantity: {product['quantity']} \n")
        else:
            print("\nNo products found matching the search criteria.")

# Main function
def main():
    while True:
        inventory_exists = str(check_inventory_file_exists()) # Check if the inventory JSON file exists, and create it if it does not
        if inventory_exists == "True":
            inventory_message = "\ninventory.json found. \ninventory loaded successfully."
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
        