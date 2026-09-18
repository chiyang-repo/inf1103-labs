
def get_valid_input(user_input):
    input = user_input
    try:
        if int(input) < 0: # Check if user input is a negative number
            print("\nInvalid input. Please enter a non-negative number.")
            return None
        else:
            return int(input)
    except ValueError:
        if input.lower() == 'quit': #exit the program if user types 'quit'
            return 'quit' #Exit the loop and program
        else: # Increment failed entry
            print("\nInvalid input. Please enter a valid number or type 'quit' to exit.")
            return None
        



def process_delivery(quantity, cost_per_unit):
    return quantity * cost_per_unit

def calculate_tax(delivery_cost):
    tax_rate = 0.10
    return delivery_cost * tax_rate

def generate_report(inventory, delivery_cost, count):
    print("\n--- Delivery Report ---")
    print(f"Total Deliveries Processed: {inventory}")
    print(f"Total Delivery Cost: {delivery_cost}")
    print(f"Number of Failed/Rejected Entries: {count}")


def main():
    # Inventory stocks
    inventory = 0
    count = 0
    cost_per_unit = 0.5
    while True:
        print(f"\nCurrent inventory: {inventory}") # Display current inventory
        user_input = input("\nEnter the number of items to add/update to inventory (or type 'quit' to quit): ") # Get user input
        validated_user_input = get_valid_input(user_input)
        if validated_user_input != 'quit' and validated_user_input is not None: # Check if user input is not 'quit' and not a failed entry
            if validated_user_input > 0 : # Check if user input is not zero
                inventory += validated_user_input # Increment inventory by user input
                print(f"\nInventory updated. Current stock: {inventory}")
            else:
                print("\n No changes made.")
        elif validated_user_input is None:
            count += 1 # Increment failed entry
        else:
            delivery_cost = process_delivery(inventory, cost_per_unit)
            tax = calculate_tax(delivery_cost)
            report = generate_report(inventory, delivery_cost, count)
            break
main()
        