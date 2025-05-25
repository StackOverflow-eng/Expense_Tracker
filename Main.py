import csv
import matplotlib.pyplot as plt
from datetime import datetime
from typing import List, Dict


class ExpenseTracker:
    def __init__(self, filename: str = "expenses.csv"):
        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create CSV file with headers if it doesn't exist"""
        try:
            with open(self.filename, 'x', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Amount", "Category", "Date"])
        except FileExistsError:
            pass

    def add_expense(self, amount: float, category: str) -> bool:
        """Add a new expense entry"""
        try:
            with open(self.filename, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([amount, category, datetime.now().strftime("%Y-%m-%d")])
            return True
        except Exception as e:
            print(f"Error saving expense: {e}")
            return False

    def get_expenses(self) -> List[Dict]:
        """Retrieve all expenses"""
        expenses = []
        try:
            with open(self.filename, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    expenses.append(row)
        except Exception as e:
            print(f"Error reading expenses: {e}")
        return expenses

    def get_spending_by_category(self) -> Dict[str, float]:
        """Calculate total spending per category"""
        expenses = self.get_expenses()
        spending = {}
        for expense in expenses:
            category = expense["Category"]
            amount = float(expense["Amount"])
            spending[category] = spending.get(category, 0) + amount
        return spending

    def generate_report(self):
        """Generate a pie chart visualization"""
        spending = self.get_spending_by_category()

        if not spending:
            print("No expenses to visualize.")
            return

        categories = list(spending.keys())
        amounts = list(spending.values())

        plt.figure(figsize=(8, 6))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
        plt.title("Your Expense Distribution")
        plt.show()


def display_menu():
    print("\n💰 Expense Tracker CLI")
    print("1. ➕ Add Expense")
    print("2. 📊 View Spending Report")
    print("3. 🚪 Exit")


def main():
    tracker = ExpenseTracker()

    while True:
        display_menu()
        choice = input("> Select an option (1-3): ").strip()

        if choice == "1":
            try:
                amount = float(input("Enter amount ($): "))
                category = input("Enter category (e.g., Food, Rent): ").capitalize()
                if tracker.add_expense(amount, category):
                    print("✅ Expense added successfully!")
            except ValueError:
                print("❌ Invalid amount. Please enter a number.")

        elif choice == "2":
            print("\n📈 Generating spending report...")
            tracker.generate_report()

        elif choice == "3":
            print("👋 Exiting...")
            break

        else:
            print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    main()
