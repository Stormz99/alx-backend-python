from seed import connect_to_prodev

def stream_user_ages():
    connection = connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    for (age,) in cursor:
        yield int(age)
    cursor.close()
    connection.close()

def calculate_average_age():
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1
    return total / count if count else 0
