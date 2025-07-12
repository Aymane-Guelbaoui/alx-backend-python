import mysql.connector
from seed import connect_to_prodev

def stream_users():
    conn = connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row
    cursor.close()
    conn.close()
