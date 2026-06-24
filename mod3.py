
print("Welcome to the Recycling Tracker")

# Recycling item menu
print("\nRecyclable Item Types:")
print("1. Plastic")
print("2. Aluminum")
print("3. Glass")
print("4. Cardboard")
print("5. Paper")

total_items = 0
total_weight = 0.0

try:
    num_items = int(input("\nEnter the number of recyclable items collected: "))

    for i in range(num_items):
        item_number = int(input(f"\nEnter the item number for recyclable item #{i + 1}: "))

        if item_number == 1:
            item_type = "Plastic"
        elif item_number == 2:
            item_type = "Aluminum"
        elif item_number == 3:
            item_type = "Glass"
        elif item_number == 4:
            item_type = "Cardboard"
        elif item_number == 5:
            item_type = "Paper"
        else:
            item_type = "Unknown"

        weight = float(input(f"Enter the weight (in pounds) of the {item_type}: "))

        total_items += 1
        total_weight += weight

    average_weight = total_weight / total_items

    print("\n--- Recycling Statistics ---")
    print(f"Total Items Recycled: {total_items}")
    print(f"Total Weight Recycled: {total_weight:.2f} pounds")
    print(f"Average Weight Per Item: {average_weight:.2f} pounds")
    print(f"Estimated Waste Diverted from Landfills: {total_weight:.2f} pounds")

except ValueError:
    print("\nError: Please enter valid numeric values.")

except ZeroDivisionError:
    print("\nError: At least one recyclable item must be entered.")

finally:
    print("\nThank you for helping reduce waste and protect the environment!")
    print("Program Ended.")

