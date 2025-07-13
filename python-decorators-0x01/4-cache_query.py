import time
import sqlite3
import functools

# Simple in-memory cache
query_cache = {}

def with_db_connection(func):
    """Decorator to provide a database connection to the wrapped function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def cache_query(func):
    """Decorator to cache the results of a query."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get("query") or (args[1] if len(args) > 1 else None)
        if query in query_cache:
            print("Returning cached result for:", query)
            return query_cache[query]
        
        print("Executing query:", query)
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """Fetch users from the database."""
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call: executes the query
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call: uses cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")

# Output results
print("Fetched users:", users)
print("Fetched users again (should be cached):", users_again)
