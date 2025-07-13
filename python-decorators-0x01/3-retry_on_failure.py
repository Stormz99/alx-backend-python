import time
import sqlite3
import functools

def with_db_connection(func):
    """Decorator that provides a database connection to the wrapped function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def retry_on_failure(retries=3, delay=2):
    """
    Decorator that retries the decorated function if it raises an exception.
    
    Parameters:
        retries (int): Number of times to retry.
        delay (int): Delay between retries in seconds.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[Retry {attempt}] Failed: {e}")
                    last_exception = e
                    if attempt < retries:
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """
    Function to fetch users from the database. Automatically retries if it fails.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

if __name__ == "__main__":
    try:
        users = fetch_users_with_retry()
        print("Fetched users:", users)
    except Exception as e:
        print(f"Final failure after retries: {e}")
