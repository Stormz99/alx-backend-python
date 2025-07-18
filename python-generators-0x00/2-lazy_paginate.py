from seed import connect_to_prodev

def paginate_users(page_size, offset):
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (page_size, offset))
    rows = cursor.fetchall()
    connection.close()
    return rows

def lazy_paginate(page_size):
    offset = 0
    while True:
        page = paginate_user(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size