import sqlite3
import functools
from datetime import datetime 

def log_queries(func):
    """Decorator to log SQL queries with a timestamp."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else '')
        print(f"{datetime.now()} - Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Call the function with a query
users = fetch_all_users(query="SELECT * FROM users")