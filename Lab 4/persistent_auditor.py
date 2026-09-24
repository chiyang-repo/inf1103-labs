import csv
import re
from datetime import datetime

def load_inventory():
    try:
        with open("inventory.csv", 'r') as file:
            reader = csv.reader(file)
            inventory_data = list(reader)
            inventory = ""
            if len(inventory_data) > 0:
                for row in range(1, len(inventory_data)):  # Skip the header row
                    inventory += (f"""
{inventory_data[row][0]}, {inventory_data[row][1]}, {inventory_data[row][2]}, {inventory_data[row][3]}""")
                return inventory
            else:
                return "Inventory is currently empty."
    except FileNotFoundError:
        initialize_inventory_file()
        return "Inventory file not found. Starting with an empty inventory."
        


def initialize_inventory_file():
    with open("inventory.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "PRODUCT_NAME", "QUANTITY", "PRICE"])  # Write the header row
        print("Inventory file created.")

def add_items():
    with open("inventory.csv", 'r', newline='') as file:
        reader = csv.reader(file)
        inventory_data = list(reader)
        product_id = len(inventory_data)  # Get the next product ID based on the number of existing rows
    with open("inventory.csv", 'a', newline='') as file:
        while True:
            product_name = input("Enter the product name: ")
            product_quantity = input("Enter the product quantity: ")
            product_price = input("Enter the product price: ")
            valid_product = validate_product_entry(product_name,product_quantity,product_price)
            if valid_product is True:
                # Write the product data to the CSV file
                writer = csv.writer(file)
                writer.writerow([product_id, product_name, product_quantity, round(float(product_price), 2)])
                print("Product added successfully.")
                transactional_history("ADDED", product_name, product_quantity, product_price)
                break
            else:
                print("Invalid product entry. Please try again.")
                
def update_items():
    with open("inventory.csv", 'r', newline='') as file:
        reader = csv.reader(file)
        inventory_data = list(reader)
        if len(inventory_data) <= 1:  # Check if there are any products in the inventory
            print("No products available to update.")
            return
        print("\nCurrent Inventory:")
        for row in range(1, len(inventory_data)):  # Skip the header row
            print(f"{inventory_data[row][0]}, {inventory_data[row][1]}, {inventory_data[row][2]}, {inventory_data[row][3]}")
        while True:
            product_id = input("Enter the product ID to update: ")
            if not product_id.isdigit() or int(product_id) < 1 or int(product_id) >= len(inventory_data):
                print("Invalid product ID. Please try again.")
                continue
            product_name = input("Enter the new product name: ")
            product_quantity = input("Enter the new product quantity: ")
            product_price = input("Enter the new product price: ")
            valid_product = validate_product_entry(product_name,product_quantity,product_price)
            if valid_product is True:
                # Update the product data in the CSV file
                inventory_data[int(product_id)][1] = product_name
                inventory_data[int(product_id)][2] = product_quantity
                inventory_data[int(product_id)][3] = round(float(product_price), 2)
                with open("inventory.csv", 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(inventory_data)
                print("\nProduct updated successfully.")
                transactional_history("UPDATED", product_name, product_quantity, product_price)
                break
            else:
                print("Invalid product entry. Please try again.")

def transactional_history(action, product_name, product_quantity, product_price):
    with open("inventory.txt", 'a') as file:
        file.write(f"[{datetime.now()}] {action}: {product_name}, Quantity: {product_quantity}, Price: {product_price}\n")
    return

def order_list():
    with open("inventory.csv", 'r', newline='') as file:
        reader = csv.reader(file)
        inventory_data = list(reader)
        if len(inventory_data) <= 1:  # Check if there are any products in the inventory
            print("No products available to create an order list.")
            return
        else:
            print("\nCurrent Inventory:")
            for row in range(1, len(inventory_data)):  # Skip the header row
                print(f"{inventory_data[row][0]}, {inventory_data[row][1]}, {inventory_data[row][2]}, {inventory_data[row][3]}")
            with open("orders.txt", 'w') as file:
                while True:
                    product_id = input("Enter the product ID to add to the order list: ")
                    if not product_id.isdigit() or int(product_id) < 1 or int(product_id) >= len(inventory_data):
                        print("Invalid product ID. Please try again.")
                    else:
                        while True:
                            order_quantity = input("Enter the quantity to order: ")
                            if not order_quantity.isdigit() or int(order_quantity) < 1 or int(order_quantity) > int(inventory_data[int(product_id)][2]):
                                print("Invalid quantity. Please try again.")
                            else:
                                break
                        product_name = inventory_data[int(product_id)][1]
                        product_quantity = inventory_data[int(product_id)][2]
                        product_price = inventory_data[int(product_id)][3]
                        save_inventory(product_quantity, order_quantity, product_id)
                        file.write(f"[{datetime.now()}] ORDERED: {product_name}, Quantity: {order_quantity}, Price: {round(float(product_price) * int(order_quantity), 2)}\n")
                        print("\nOrder successfully added to orders.txt.")
                        break

def save_inventory(product_quantity, order_quantity, product_id):
    with open("inventory.csv", 'r', newline='') as file:
        reader = csv.reader(file)
        inventory_data = list(reader)
        updated_product_quantity = int(product_quantity) - int(order_quantity)
        if updated_product_quantity == 0:
            inventory_data.pop(int(product_id))  # Remove the product from the inventory if quantity is zero
            for row in range(1, len(inventory_data)):  # Update the product IDs for the remaining products
                inventory_data[row][0] = str(row)
            with open("inventory.csv", 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(inventory_data)
                print("\nInventory updated successfully.")
        else:
            inventory_data[int(product_id)][2] = str(updated_product_quantity)  # Update the product quantity in the inventory
            with open("inventory.csv", 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(inventory_data)
            print("\nInventory updated successfully.")


def validate_product_entry(product_name, product_quantity, product_price):
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

# Main function
def main():
    while True:
        inventory = load_inventory()  # Load the current inventory from the CSV file
        user_choice = input(f"""\nWelcome to the Persistent Auditor Program!
        \nCurrent inventory is displayed below:{inventory}
        \nThis program allows you to manage your inventory by adding new products and updating existing ones.
        \nChoose which action you would like to do:
1. Add a new product to the inventory
2. Update an existing product in the inventory
3. Create an order list based on the current inventory
4. Exit the program\n
Input your choice (1-4):""")
        match user_choice:
            case "1": add_items()
            case "2": update_items()
            case "3": order_list()
            case "4": 
                print("\nExiting the program.")
                break
            case _: print("Invalid choice. Please try again.\n")
    
main()
        