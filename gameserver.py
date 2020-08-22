import socket
from _thread import *
from board import *

class GameServer:

    def __init__(self, name, ip, port, gameid, min, max, blind):
        self.board = Board(gameid, name, min, max, blind)
        self.name = name
        self.ip = ip
        self.port = port
        self.addr = (self.ip, self.port)
        self.format = "utf-8"
        self.header = 2048
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.addr)
        print(f'Name={self.name} IP={self.ip} PORT={self.port} has started')
        self.connect_players()

    def connect_client(self, conn):
        connected = True
        while connected:
            try:
                msg_length = conn.recv(self.header).decode(self.format)
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(self.format)
                if msg == "bye":
                    connected = False
                if msg == "REFRESH":
                    message = "TONY"
                    msg = message.encode(self.format)
                    msg_length = len(msg)
                    send_length = str(msg_length).encode(self.format)
                    send_length += b' ' * (self.header - len(send_length))
                    conn.send(send_length)
                    conn.send(msg)

            except:
                break

        print("Connection Closed")
        conn.close()

    def connect_players(self):
        self.server.listen(4)
        while True:
            conn, addr = self.server.accept()
            print(addr, " has connected to server")
            start_new_thread(self.connect_client, (conn,))



