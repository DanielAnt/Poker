import socket
from _thread import *

class Lobby_client():

    def __init__(self, ip=None, port=None):
        if ip and port:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.host_ip = ip
            self.host_port = port
            self.addr = (self.host_ip, self.host_port)
            self.format = "utf-8"
            self.client.connect(self.addr)
            #self.refresh_lobbys()



    def refresh_lobbys(self):
        self.client.send()
        print(self.client.recv(2048).decode())

    def send(self,message):
        header = 64
        msg = message.encode(self.format)
        msg_length = len(msg)
        send_length = str(msg_length).encode(self.format)
        send_length += b' ' * (header - len(send_length))
        self.client.send(send_length)
        self.client.send(msg)


        msg_length = self.client.recv(header).decode(self.format)
        msg_length = int(msg_length)
        msg = self.client.recv(msg_length).decode(self.format)
        print(msg)


        if message == "bye":
            quit()


new_client = Lobby_client(ip = "192.168.1.132", port = 16000)
