import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create the users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    email TEXT NOT NULL UNIQUE
)
""")

# Insert sample data into the users table
cursor.execute("INSERT INTO users (name, age, email) VALUES (?, ?, ?)", ('Alice', 30, 'alice@example.com'))
cursor.execute("INSERT INTO users (name, age, email) VALUES (?, ?, ?)", ('Bob', 25, 'bob@example.com'))
cursor.execute("INSERT INTO users (name, age, email) VALUES (?, ?, ?)", ('Charlie', 28, 'charlie@example.com'))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database initialized and sample data inserted.")
