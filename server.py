import socket
from _thread import *
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
clientid = 0

#print(socket.gethostname())

try:
    s.bind((SERVER, PORT))
except socket.error as e:
    print(str(e))



def connect_client(conn):
global clientid



   while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                print("Recieved: " + reply)
                arr = reply.split(":")

                reply = pos[nid][:]
                print("Sending: " + reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Connection Closed")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    start_new_thread(connect_client, (conn,))