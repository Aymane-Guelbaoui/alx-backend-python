from seed import connect_to_prodev

def paginate_users(page_size, offset):
    conn = connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def lazy_pagination(page_size):
    offset = 0
    while True:
        users = paginate_users(page_size, offset)
        if not users:
            break
        yield users
        offset += page_size
