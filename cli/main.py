import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.budget import Category, Transaction

import sqlite3

def add_category():
    name = input("Enter category name: ")
    category = Category(name)
    category.save()
    print(f"Category '{name}' added successfully.")

def add_income():
    description = input("Enter income description: ")
    amount = float(input("Enter income amount: "))
    category_id = select_category()
    transaction = Transaction(description, amount, category_id)
    transaction.save()
    print(f"Income transaction '{description}' added successfully.")

def add_expense():
    description = input("Enter expense description: ")
    amount = float(input("Enter expense amount: "))
    category_id = select_category()
    transaction = Transaction(description, -amount, category_id)  # Expense amount is negative
    transaction.save()
    print(f"Expense transaction '{description}' added successfully.")

def view_transactions():
    transactions = Transaction.get_all()
    if not transactions:
        print("No transactions found.")
    else:
        print("All Transactions:")
        for transaction in transactions:
            print(f"ID: {transaction[0]}, Description: {transaction[1]}, Amount: {transaction[2]}, Category ID: {transaction[3]}")

def view_balance():
    category_id = select_category()
    transactions = Transaction.find_by_category(category_id)
    if not transactions:
        print("No transactions found for this category.")
    else:
        balance = sum(transaction[2] for transaction in transactions)
        print(f"Current Balance for Category ID {category_id}: {balance}")

def select_category():
    categories = Category.get_all()
    if not categories:
        print("No categories found. Please add a category first.")
        add_category()
        return select_category()
    else:
        print("Select a Category:")
        for category in categories:
            print(f"ID: {category[0]}, Name: {category[1]}")
        category_id = int(input("Enter Category ID: "))
        while not Category.find_by_id(category_id):
            print("Invalid Category ID. Please select a valid Category ID.")
            category_id = int(input("Enter Category ID: "))
        return category_id

def main():
    # Initialize database tables if they don't exist
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    ''')
    conn.commit()
    conn.close()

    # Main loop for CLI
    while True:
        print("\nBudget Tracker Menu")
        print("1. Add Category")
        print("2. Add Income")
        print("3. Add Expense")
        print("4. View Transactions")
        print("5. View Balance")
        print("6. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            add_category()
        elif choice == '2':
            add_income()
        elif choice == '3':
            add_expense()
        elif choice == '4':
            view_transactions()
        elif choice == '5':
            view_balance()
        elif choice == '6':
            print("Exiting the Budget Tracker. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == '__main__':
    main()
