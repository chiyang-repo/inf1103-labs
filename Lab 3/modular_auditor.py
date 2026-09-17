# Inventory stocks
inventory = 0
count = 0

cost_per_unit = 0.5


def get_valid_input(user_input):
    input = user_input 
    if input.isdigit() == False:
        if input.lower() == 'quit': #exit the program if user types 'quit'
            print(f"\nYou have exited the program. \nTotal unit processed: {inventory} \nTotal number of failed entries: {count}")
            return 'quit' #Exit the loop and program
        else: # Increment failed entry
            count += 1
            print("\nInvalid input. Please enter a valid number or type 'quit' to exit.")
            return None
    else:
        return int(input)

def process_delivery(quantity, cost_per_unit):
    return quantity * cost_per_unit

def calculate_tax(delivery_cost):
    tax_rate = 0.10
    return delivery_cost * tax_rate

while True:
    print(f"\nCurrent inventory: {inventory}") # Display current inventory
    user_input = input("\nEnter the number of items to add/update to inventory (or type 'quit' to quit): ") # Get user input
    validated_user_input = get_valid_input(user_input)
    if validated_user_input != 'quit' and validated_user_input is not None:
        if validated_user_input < 0: # Check if user input is a negative number
            count += 1 # Increment failed entry
            print("\nInvalid input. Please enter a non-negative number.")
        else: #Successful entry
            inventory += validated_user_input # Increment inventory by user input
            print(f"\nInventory updated. Current stock: {inventory}")
    else:
        delivery_cost = process_delivery(inventory, cost_per_unit)
        tax = calculate_tax(delivery_cost)
        report = generate_report(inventory, delivery_cost, tax)
        



# Get user input for the number of items to add to inventory
while True:
    # Check if inventory is less than 500
    if inventory < 500:
        print(f"\nCurrent inventory: {inventory}") # Display current inventory
        user_input = input("\nEnter the number of items to add/update to inventory (or type 'quit' to quit): ") # Get user input
        # Check if user input is a digit or string
        if user_input.isdigit() == False:
            if user_input == 'quit': #exit the program if user types 'quit'
                print(f"\nYou have exited the program. \nTotal unit processed: {inventory} \nTotal number of failed entries: {count}")
                break #Exit the loop and program
            else: # Increment failed entry
                count += 1
                print("\nInvalid input. Please enter a valid number or type 'quit' to exit.")
        elif int(user_input) < 0: # Check if user input is a negative number
            count += 1 # Increment failed entry
            print("\nInvalid input. Please enter a non-negative number.")
        else: #Successful entry
            inventory += int(user_input) # Increment inventory by user input
            print(f"\nInventory updated. Current stock: {inventory}")
    else: # Inventory limit reached
        count += 1 # Increment failed entry
        print("\nInventory limit reached. Cannot add more items.\nTotal unit processed: {inventory} \nTotal number of failed entries: {count}")
        break #Exit the loop and program

        
        