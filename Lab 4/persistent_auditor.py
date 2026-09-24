import csv
import os
import re

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
                print("Product updated successfully.")
                break
            else:
                print("Invalid product entry. Please try again.")

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
        user_choice = input(f"""Welcome to the Persistent Auditor Program!
        \nCurrent inventory is displayed below:{inventory}
        \nThis program allows you to manage your inventory by adding new products and updating existing ones.
        \nChoose which action you would like to do:
1. Add a new product to the inventory
2. Update an existing product in the inventory
3. Create an order list based on the current inventory
4. Exit the program\n
Input your choice (1-4):""")
        match user_choice:
            case "1": print("0")
            case "2": update_items()
            case "3": print("2")
            case "4": 
                print("\nExiting the program.")
                break
            case _: print("Invalid choice. Please try again.\n")

    
    # Inventory stocks upon initialization
    """ if not os.path.exists("inventory.csv"):
        initialize_inventory_file()
        checked_inventory = load_inventory()"""
    

    """while True: 
        print(f"\nCurrent inventory: {inventory}") # Display current inventory
        user_input = input("\nEnter the number of items to add/update to inventory (or type 'quit' to quit): ") # Get user input
        validated_user_input = get_valid_input(user_input) #run the user input through the validation function
        if validated_user_input != 'quit' and validated_user_input is not None: # Check if user input is not 'quit' and not a failed entry
            if validated_user_input > 0 : # Check if user input is not zero
                inventory += validated_user_input # Increment inventory by user input
                print(f"\nInventory updated. Current stock: {inventory}")
            else:
                print("\nNo changes made.") # User input is zero, no changes made to inventory
        elif validated_user_input is None:
            count += 1 # Increment failed entry
        else:
            delivery_cost = process_delivery(inventory, cost_per_unit) # Calculate delivery cost based on inventory and cost per unit
            tax = calculate_tax(delivery_cost) # Calculate tax based on delivery cost
            report = generate_report(inventory, delivery_cost, count) # Generate report with inventory, delivery cost, and failed entry count
            break"""
main()
        