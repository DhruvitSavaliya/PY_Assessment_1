#Write a program to demonstrate the Fruit Store Console application

import json

# Fruit Manager Module
class FruitManager:
    def __init__(self, file_name="inventory.json"):
        self.file_name = file_name
        self.inventory = self.load_inventory()

    def load_inventory(self):
        """Load inventory from a file."""
        try:
            with open(self.file_name, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            print("Error reading the inventory file. Starting with an empty inventory.")
            return {}

    def save_inventory(self):
        """Save inventory to a file."""
        with open(self.file_name, "w") as file:
            json.dump(self.inventory, file)

    def add_fruit(self, fruit_name, quantity, price):
        """Add fruit to the inventory."""
        if fruit_name in self.inventory:
            self.inventory[fruit_name]['quantity'] += quantity
            self.inventory[fruit_name]['price'] = price
        else:
            self.inventory[fruit_name] = {'quantity': quantity, 'price': price}
        print(f"{fruit_name} added/updated successfully!")
        self.save_inventory()

    def view_inventory(self):
        """Display all fruits in the inventory."""
        if not self.inventory:
            print("The inventory is empty.")
        else:
            print("\nFruit Inventory:")
            print("-----------------")
            for fruit, details in self.inventory.items():
                print(f"{fruit}: Quantity = {details['quantity']}, Price = {details['price']:.2f} /-")

    def update_quantity(self, fruit_name, quantity):
        """Update the quantity of a specific fruit."""
        if fruit_name in self.inventory:
            self.inventory[fruit_name]['quantity'] += quantity
            print(f"{fruit_name} quantity updated successfully!")
            self.save_inventory()
        else:
            print(f"{fruit_name} not found in inventory.")

    def remove_fruit(self, fruit_name):
        """Remove a fruit from the inventory."""
        if fruit_name in self.inventory:
            del self.inventory[fruit_name]
            print(f"{fruit_name} removed from inventory.")
            self.save_inventory()
        else:
            print(f"{fruit_name} not found in inventory.")

# Customer Module
class Customer:
    def __init__(self, fruit_manager):
        self.fruit_manager = fruit_manager

    def buy_fruit(self, fruit_name, quantity):
        """Allow the customer to buy fruits."""
        if fruit_name in self.fruit_manager.inventory:
            available_quantity = self.fruit_manager.inventory[fruit_name]['quantity']
            price_per_unit = self.fruit_manager.inventory[fruit_name]['price']

            if quantity <= available_quantity:
                total_cost = quantity * price_per_unit
                self.fruit_manager.inventory[fruit_name]['quantity'] -= quantity
                print(f"You bought {quantity} {fruit_name}(s) for {total_cost:.2f} /-.")

                # Remove fruit from inventory if quantity becomes zero
                if self.fruit_manager.inventory[fruit_name]['quantity'] == 0:
                    self.fruit_manager.remove_fruit(fruit_name)
                else:
                    self.fruit_manager.save_inventory()
            else:
                print(f"Sorry, only {available_quantity} {fruit_name}(s) available.")
        else:
            print(f"{fruit_name} is not available in the inventory.")

# Menu Execution
class FruitStoreApp:
    def __init__(self):
        self.fruit_manager = FruitManager()
        self.customer = Customer(self.fruit_manager)

    def display_menu1(self):
        print("\nManager Menu:")
        print("1. Add Fruit to Inventory")
        print("2. View Inventory")
        print("3. Update Fruit Quantity")
        print("4. Remove Fruit from Inventory")
        print("5. Exit")
    
    def display_menu2(self):
        print("\nCustomer Menu:")
        print("1. View Fruit Stock")
        print("2. Buy Fruit")
        print("3. Exit")

    def manager_run(self):
        while True:
            self.display_menu1()
            try:
                choice = int(input("\nEnter your choice: "))
                if choice == 1:
                    fruit_name = input("Enter fruit name: ").strip()
                    quantity = int(input("Enter quantity: "))
                    price = float(input("Enter price per unit: "))
                    self.fruit_manager.add_fruit(fruit_name, quantity, price)
                elif choice == 2:
                    self.fruit_manager.view_inventory()
                elif choice == 3:
                    fruit_name = input("Enter fruit name: ").strip()
                    quantity = int(input("Enter quantity to add: "))
                    self.fruit_manager.update_quantity(fruit_name, quantity)
                elif choice == 4:
                    fruit_name = input("Enter fruit name to remove: ").strip()
                    self.fruit_manager.remove_fruit(fruit_name)
                elif choice == 5:
                    print("Exiting Manager Menu.")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    def customer_run(self):
        while True:
            self.display_menu2()
            try:
                choice = int(input("\nEnter your choice: "))
                if choice == 1:
                    self.fruit_manager.view_inventory()
                elif choice == 2:
                    fruit_name = input("Enter fruit name to buy: ").strip()
                    quantity = int(input("Enter quantity to buy: "))
                    self.customer.buy_fruit(fruit_name, quantity)
                elif choice == 3:
                    print("Exiting Customer Menu.")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    app = FruitStoreApp()

    while True:
        print("\nFruit Store Application")
        print("1. Manager")
        print("2. Customer")
        print("3. Exit")

        try:
            choice = int(input("Enter your role: "))
            if choice == 1:
                app.manager_run()
            elif choice == 2:
                app.customer_run()
            elif choice == 3:
                print("Thank you for using the Fruit Store application!")
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
