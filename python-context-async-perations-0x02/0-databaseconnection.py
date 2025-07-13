import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        
    def __enter__(self):
        """Establish a database connection."""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
        if exc_type is not None:
            print(f"An error occurred: {exc_value}")
        return False  # Propagate exceptions


# Create table and insert data
with DatabaseConnection("user.db") as conn:
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        );
    ''')
    cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', ('Alice', "alice@example.com"))
    cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', ('John Doe', "joedoe@example.com"))
    conn.commit()

# Fetch and display users
with DatabaseConnection("user.db") as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    results = cursor.fetchall()
    print(f"Users in the database: {results}")
