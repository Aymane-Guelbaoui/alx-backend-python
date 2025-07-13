from seed import connect_to_prodev

def stream_users_in_batches(batch_size):
    """Generator function that yields rows in batches from the user_data table"""
    conn = connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    offset = 0
    while True:
        cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (batch_size, offset))
        rows = cursor.fetchall()
        if not rows:
            break
        yield rows 
        offset += batch_size
    cursor.close()
    conn.close()


def batch_processing(batch_size):
    """Processes each batch to filter users over the age of 25"""
    for batch in stream_users_in_batches(batch_size):  # loop 1
        for user in batch: 
            if user["age"] > 25:
                print(user)  


return 
