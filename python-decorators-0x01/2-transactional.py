import sqlite3
import functools

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

def transactional(func):
    """Decorator to handle DB transactions (commit/rollback)."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            print(f"Transaction failed: {e}")
            raise
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    if cursor.rowcount == 0:
        raise ValueError(f"No user found with ID {user_id}")
    return cursor.rowcount

update_user_email(user_id=2, new_email="Not_Charlie@example.com")