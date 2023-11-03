# Importing the 'requests' library for making HTTP requests.
import requests
from datetime import datetime

# Class for ID Verification Service
class IDVerificationService:
    # Initializing the service with an API key.
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://id-verification-service.com/api/"

    # Method to verify an ID number.
    def verify_id(self, id_number):
        url = f"{self.base_url}verify"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {"id_number": id_number}

        # Sending a POST request to the ID verification service.
        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            result = response.json()
            return result["verified"]
        else:
            raise Exception(f"ID verification failed. Status code: {response.status_code}")

# Class for the Point of Sale system
class PointOfSale:
    # Initializing the PointOfSale class.
    def __init__(self):
        # Defining the menu with item IDs, names, and prices.
        self.menu = {
            1: {
                "item": "Soda",
                "options": {
                    1: ("Cola", 2.50),
                    2: ("Lemon-Lime", 2.50),
                    3: ("Root Beer", 2.50),
                }
            },
            2: {
                "item": "Burger",
                "options": {
                    1: ("Classic", 8.50),
                    2: ("Cheese", 9.00),
                    3: ("Bacon", 9.50),
                }
            },
            3: {
                "item": "Fries",
                "options": {
                    1: ("Regular", 3.00),
                    2: ("Curly", 3.50),
                    3: ("Sweet Potato", 4.00),
                }
            },
            4: {
                "item": "Salad",
                "options": {
                    1: ("Caesar", 5.50),
                    2: ("Greek", 6.00),
                    3: ("Cobb", 6.50),
                }
            },
            5: {
                "item": "Pizza",
                "options": {
                    1: ("Margherita", 10.00),
                    2: ("Pepperoni", 11.00),
                    3: ("Vegetarian", 12.00),
                }
            },
            6: {
                "item": "Wine",
                "options": {
                    1: ("Red", 12.00),
                    2: ("White", 10.00),
                    3: ("Rose", 11.00),
                },
                "alcohol": True
            },
            7: {
                "item": "Beer",
                "options": {
                    1: ("IPA", 5.00),
                    2: ("Lager", 4.50),
                    3: ("Stout", 5.50),
                },
                "alcohol": True
            },
            8: {
                "item": "Cocktail",
                "options": {
                    1: ("Mojito", 8.00),
                    2: ("Martini", 9.00),
                    3: ("Margarita", 8.50),
                },
                "alcohol": True
            },
            9: {
                "item": "Pasta",
                "options": {
                    1: ("Spaghetti Bolognese", 9.50),
                    2: ("Alfredo", 10.00),
                    3: ("Pesto", 10.50),
                }
            },
            10: {
                "item": "Ice Cream",
                "options": {
                    1: ("Vanilla", 4.00),
                    2: ("Chocolate", 4.00),
                    3: ("Strawberry", 4.00),
                }
            }
        }
        self.order = []  # Initializing an empty order list.

    # Method to display a welcome message.
    def welcome_message(self):
        print("Welcome to the Beach Side Restaurant!\n")

    # Method for employee to verify customer's age.
    def employee_verify_age(self):
        # Asking for the customer's birthday.
        birthday = input("Please enter the customer's birthday (YYYY-MM-DD): ")

        # Checking if the entered date is a valid date.
        try:
            birthdate = datetime.strptime(birthday, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
            return False

        # Calculating the age based on the entered birthday.
        today = datetime.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

        # Checking if the customer is at least 21 years old.
        if age >= 21:
            return True
        else:
            print("Customer is not of legal drinking age (21 years or older).")
            return False

    # Method to display the menu.
    def display_menu(self):
        print("Menu:")
        for item_id, item_info in self.menu.items():
            print(f"{item_id}. {item_info['item']} - ${item_info['options'][1][1]:.2f}")

    # Method to take the customer's order.
    def take_order(self):
        while True:
            try:
                # Asking for the item ID from the customer.
                item_id = int(input("\nEnter the ID of the item you'd like to order (or 0 to finish): "))
                if item_id == 0:
                    break
                elif item_id not in self.menu:
                    print("Invalid item ID. Please try again.")
                    continue
                if self.menu[item_id].get("alcohol"):
                    if not self.employee_verify_age():
                        print("Customer is not allowed to order alcohol.")
                        continue
                # Asking for the quantity of the item.
                quantity = int(input(f"How many {self.menu[item_id]['item']} would you like? (1-9): "))
                if quantity < 1 or quantity > 9:
                    print("Invalid quantity. Please enter a number between 1 and 9.")
                    continue
                # Adding the item to the order list.
                self.order.append((self.menu[item_id]["item"], quantity, self.menu[item_id]["options"][1][1]))
            except ValueError:
                print("Invalid input. Please enter a valid number.")
                continue

    # Method to display the order summary.
    def display_order_summary(self):
        if not self.order:
            print("\nNo items ordered.")
            return

        print("\nOrder Summary:")
        for item_name, quantity, item_price in self.order:
            subtotal = quantity * item_price
            print(f"{item_name} x{quantity}: ${subtotal:.2f}")
        grand_total = sum(quantity * item_price for _, quantity, item_price in self.order)
        print(f"\nGrand Total: ${grand_total:.2f}")

    # Method to process the customer's order.
    def process_order(self):
        self.welcome_message()
        self.display_menu()
        self.take_order()
        self.display_order_summary()

        if self.order:
            self.handle_payment()

    # Method for handling payment.
    def handle_payment(self):
        while True:
            try:
                # Asking for the amount paid by the customer.
                amount_paid = float(input("\nEnter the amount paid: $"))
                grand_total = sum(quantity * item_price for _, quantity, item_price in self.order)
                if amount_paid < grand_total:
                    print("Insufficient payment. Please enter a valid amount.")
                    continue
                change = amount_paid - grand_total
                print(f"\nChange: ${change:.2f}")
                self.generate_receipt()
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    # Method to generate the receipt.
    def generate_receipt(self):
        print("\nReceipt:")
        for item_name, quantity, item_price in self.order:
            subtotal = quantity * item_price
            print(f"{item_name} x{quantity}: ${subtotal:.2f}")
        grand_total = sum(quantity * item_price for _, quantity, item_price in self.order)
        print(f"\nGrand Total: ${grand_total:.2f}")
        print("Thank you for dining with us!")

# Main code block to run the PointOfSale class.
if __name__ == "__main__":
    pos = PointOfSale()
    pos.process_order()
