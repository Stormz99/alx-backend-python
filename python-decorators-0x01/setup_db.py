import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    age INTEGER
)
''')

cursor.executemany(
    'INSERT INTO users (name, email, age) VALUES (?, ?, ?)',
    [
        ("Alice", "alice@example.com", 30),
        ("Bob", "bob@example.com", 45),
        ("Charlie", "charlie@example.com", 22),
    ]
)

conn.commit()
conn.close()

print(f" users.db created and populated")
