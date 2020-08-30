import socket
from _thread import *
import pickle
from gameserver import GameServer


class LobbyServer:

    def __init__(self):
        self.SERVER = "192.168.1.132"
        self.PORT = 16000
        self.ADDR = (self.SERVER, self.PORT)
        self.format = "utf-8"
        self.header = 128
        self.game_servers_list = []
        self.game_port = self.PORT
        self.game_id = 10000
        self.start_server()

    def connect_client(self, user,addr):
        connected = True
        while connected:
            try:
                msg_length = user.recv(self.header).decode(self.format)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = user.recv(msg_length).decode(self.format)
                    if msg == "bye":
                        connected = False
                    elif msg == "REFRESH":
                        if len(self.game_servers_list) > 0:
                            msg = pickle.dumps(self.game_servers_list)
                            msg_length = len(msg)
                            send_length = str(msg_length).encode(self.format)
                            send_length += b' ' * (self.header - len(send_length))
                            user.send(send_length)
                            user.send(msg)
                        else:
                            message = "empty"
                            msg = message.encode(self.format)
                            msg_length = len(msg)
                            send_length = str(msg_length).encode(self.format)
                            send_length += b' ' * (self.header - len(send_length))
                            user.send(send_length)
                            user.send(msg)
                    elif msg == "NEWTABLE":
                        self.create_new_table(user)
            except Exception as e:
                print(e)
                break
        print(f"{addr} disconnected")
        user.close()

    def create_new_table(self, user):
        msg_length = user.recv(self.header).decode(self.format)
        if msg_length:
            msg_length = int(msg_length)
            msg = user.recv(msg_length).decode(self.format)
            print(msg)
            start_new_thread(self.new_game_server, (msg,))

    def new_game_server(self, msg):
        name, min_buyin, max_buyin, blind = msg.split(";")
        self.game_id += 1
        self.game_port += 1
        self.game_servers_list.append([self.game_id, name, self.SERVER, self.game_port, min_buyin, max_buyin, blind])
        GameServer(name, self.SERVER, self.game_port, self.game_id, min_buyin, max_buyin, blind)

    def start_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        print(f'[{self.SERVER}], STARTED')
        self.server.listen()
        while True:
            conn, addr = self.server.accept()
            print("Connected to: ", addr)
            start_new_thread(self.connect_client, (conn,addr,))


lobby_server = LobbyServer()