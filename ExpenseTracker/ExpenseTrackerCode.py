import pandas as pd
import sqlite3
import os

class ExpenseTracker:
    def __init__(self, db_name='expenses.db', csv_file='expenses.csv'):
        self.db_name = db_name
        self.csv_file = csv_file
        self.create_table()

    def create_table(self):
        """Create a SQLite database table if it doesn't exist."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY,
                date TEXT,
                category TEXT,
                amount REAL,
                description TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def add_expense(self, date, category, amount, description):
        """Add a new expense to the database and CSV file."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO expenses (date, category, amount, description)
            VALUES (?, ?, ?, ?)
        ''', (date, category, amount, description))
        conn.commit()
        conn.close()

        # Also save to CSV
        self.save_to_csv(date, category, amount, description)

    def save_to_csv(self, date, category, amount, description):
        """Save the expense to a CSV file."""
        if not os.path.isfile(self.csv_file):
            # Create a new CSV file with headers if it doesn't exist
            df = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])
            df.to_csv(self.csv_file, index=False)

        # Append the new expense to the CSV file
        df = pd.read_csv(self.csv_file)
        new_expense = pd.DataFrame([[date, category, amount, description]], columns=['Date', 'Category', 'Amount', 'Description'])
        df = pd.concat([df, new_expense], ignore_index=True)
        df.to_csv(self.csv_file, index=False)

    def view_expenses(self):
        """View all expenses from the database."""
        conn = sqlite3.connect(self.db_name)
        df = pd.read_sql_query('SELECT * FROM expenses', conn)
        conn.close()
        return df

    def delete_expense(self, expense_id):
        """Delete an expense by ID."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
        conn.close()

        # Update CSV file
        self.update_csv()

    def update_csv(self):
        """Update the CSV file to reflect the current state of the database."""
        conn = sqlite3.connect(self.db_name)
        df = pd.read_sql_query('SELECT * FROM expenses', conn)
        conn.close()
        df.to_csv(self.csv_file, index=False)

# Example usage
if __name__ == "__main__":
    tracker = ExpenseTracker()

    # Adding expenses
    tracker.add_expense('2023-10-01', 'Food', 50.0, 'Lunch at restaurant')
    tracker.add_expense('2023-10-02', 'Transport', 15.0, 'Bus ticket')

    # Viewing expenses
    print("Current Expenses:")
    print(tracker.view_expenses())

    # Deleting an expense
    tracker.delete_expense(1)  # Delete the expense with ID 1
    print("Expenses after deletion:")
    print(tracker.view_expenses())
