import socket

class GameClient():

    def __init__(self, ip=None, port=None):
        if ip and port:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.host_ip = str(ip)
            self.host_port = int(port)
            self.addr = (self.host_ip, self.host_port)
            self.format = "utf-8"
            self.header = 64
            self.client.connect(self.addr)

    def refresh_lobby(self):
        self.send("REFRESH")
        return self.recive()

    def send(self,message):
        msg = message.encode(self.format)
        msg_length = len(msg)
        send_length = str(msg_length).encode(self.format)
        send_length += b' ' * (self.header - len(send_length))
        self.client.send(send_length)
        self.client.send(msg)

    def recive(self):
        msg_length = self.client.recv(self.header).decode(self.format)
        msg_length = int(msg_length)
        msg = self.client.recv(msg_length).decode(self.format)
        return msg





#new_client = Lobby_client(ip="192.168.1.132", port=16000)



