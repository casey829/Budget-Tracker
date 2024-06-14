import sqlite3
from database.db import DATABASE_NAME

import sqlite3

class Category:
    def __init__(self, name):
        self.name = name
        self.id = None 

    def save(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('INSERT INTO categories (name) VALUES (?)', (self.name,))
        self.id = c.lastrowid
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT * FROM categories')
        categories = c.fetchall()
        conn.close()
        return categories

    @staticmethod
    def find_by_id(category_id):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT * FROM categories WHERE id = ?', (category_id,))
        category = c.fetchone()
        conn.close()
        return category


class Transaction:
    def __init__(self, description, amount, category_id):
        self.description = description
        self.amount = amount
        self.category_id = category_id
        self.id = None  

    def save(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('INSERT INTO transactions (description, amount, category_id) VALUES (?, ?, ?)',
                  (self.description, self.amount, self.category_id))
        self.id = c.lastrowid
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT * FROM transactions')
        transactions = c.fetchall()
        conn.close()
        return transactions

    @staticmethod
    def find_by_category(category_id):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT * FROM transactions WHERE category_id = ?', (category_id,))
        transactions = c.fetchall()
        conn.close()
        return transactions
