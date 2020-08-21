import socket
from _thread import *


SERVER = "192.168.1.132"
PORT = 16000
ADDR = (SERVER, PORT)
FORMAT = "utf-8"


def connect_client(conn):
    connected = True
    while connected:
        try:
            msg_length = conn.recv(64).decode(FORMAT)
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == "bye":
                connected = False
            if msg == "REFRESH":
                message = "TONY"
                msg = message.encode(FORMAT)
                msg_length = len(msg)
                send_length = str(msg_length).encode(FORMAT)
                send_length += b' ' * (64 - len(send_length))
                conn.send(send_length)
                conn.send(msg)
            """ 
            print(msg)
            message = "Message "
            msg = message.encode(FORMAT)
            msg_length = len(msg)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (64 - len(send_length))
            conn.send(send_length)
            conn.send(msg)
            """
        except:
            break

    print("Connection Closed")
    conn.close()


def server_start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    print(f'[{SERVER}], STARTED')
    server.listen(1)
    conn, addr = server.accept()
    print("Connected to: ", addr)
    start_new_thread(connect_client, (conn,))


server_start()
