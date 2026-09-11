# Inventory stocks
inventory = 0
count = 0

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
                break
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
        print("\nInventory limit reached. Cannot add more items.")
        break

        
        