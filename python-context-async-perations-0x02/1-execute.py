import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params if params else ()
        self.conn = None
        self.cursor = None
        
        
    def __enter__(self):
        """Establish a database connection and prepare the cursor."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        """Commit changes and close the database connection."""
        if exc_type is None:
            self.conn.commit()
        else:
            print(f"An error occurred: {exc_value}")
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        return False
    
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery("user.db", query, params) as results:
    print(f"Query results: {results}")