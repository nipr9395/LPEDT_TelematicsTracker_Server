import os
import socket
import psycopg2

# set up UDP socket
UDP_IP = '0.0.0.0'
UDP_PORT = int(os.environ.get('PORT',5000))
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = int(os.environ.get('DB_PORT'))
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

# connect to PostgreSQL database
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

#Bind to the UPD Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# listen for incoming packets and insert data into database
while True:
    data, addr = sock.recvfrom(1024)
    query = data.decode().strip()
    print(f"Received query '{query}' from {addr}")

    with conn.cursor() as cur:
        cur.execute(query)
        results = cur.fetchall()
        print(f"Query returned: {results}")

    conn.commit()