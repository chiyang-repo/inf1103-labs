import csv
import re
from datetime import datetime

# Validate user input function
def get_valid_input(user_input):
    input = user_input
    try:
        if int(input) < 0: # Check if user input is a negative number
            print("\nInvalid input. Please enter a non-negative number.")
            return None
        else:
            return int(input) # Valid input, return the integer value
    except ValueError: #catch the ValueError if user input is not a number
        if input.lower() == 'quit': #exit the program if user types 'quit'
            return 'quit' #Exit the loop and program
        else: # Increment failed entry for any other string input
            print("\nInvalid input. Please enter a valid number or type 'quit' to exit.")
            return None
        


# Process delivery function
def process_delivery(quantity, cost_per_unit):
    return quantity * cost_per_unit

# Calculate tax function
def calculate_tax(delivery_cost):
    tax_rate = 0.10
    return delivery_cost * tax_rate

# Generate report function
def generate_report(inventory, delivery_cost, count):
    print("\n--- Delivery Report ---")
    print(f"Total Deliveries Processed: {inventory}")
    print(f"Total Delivery Cost: {delivery_cost}")
    print(f"Number of Failed/Rejected Entries: {count}")

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
    with open("inventory.csv", 'a', newline='') as file:
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
                            product_quantity = input("Enter the quantity to order: ")
                            if not product_quantity.isdigit() or int(product_quantity) < 1 or int(product_quantity) > int(inventory_data[int(product_id)][2]):
                                print("Invalid quantity. Please try again.")
                            else:
                                break
                        product_name = inventory_data[int(product_id)][1]
                        product_price = inventory_data[int(product_id)][3]
                        file.write(f"[{datetime.now()}] ORDERED: {product_name}, Quantity: {product_quantity}, Price: {round(float(product_price) * int(product_quantity), 2)}\n")
                        print("\nOrder successfully added to orders.txt.")
                        break

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
        