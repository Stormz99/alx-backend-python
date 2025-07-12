import seed

def stream_users():
    with seed.connect_to_prodev() as connection:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM user_data")
            for user in cursor:
                yield user