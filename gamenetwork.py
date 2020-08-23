import socket
import pickle

class GameClient():

    def __init__(self, ip=None, port=None, client_id="100", client_name="ANDY"):
        if ip and port:
            self.client_id = client_id
            self.client_name = client_name
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.host_ip = str(ip)
            self.host_port = int(port)
            self.addr = (self.host_ip, self.host_port)
            self.format = "utf-8"
            self.header = 512
            self.client.connect(self.addr)
        else:
            print("WRONG IP AND PASSWORD")


    def login(self):
        self.send("LOGIN")
        login_message = f"{self.client_id};{self.client_name}"
        self.send(login_message)
        msg_length = self.client.recv(self.header).decode(self.format)
        msg_length = int(msg_length)
        recived_message = pickle.loads(self.client.recv(msg_length))
        return recived_message

    def update(self):
        message = "UPDATE"
        send_message = message.encode(self.format)
        msg_length = len(send_message)
        message_header = str(msg_length).encode(self.format)
        message_header += b' ' * (self.header - len(message_header))
        self.client.send(message_header)
        self.client.send(send_message)
        msg_length = self.client.recv(self.header).decode(self.format)
        msg_length = int(msg_length)
        recived_message = pickle.loads(self.client.recv(msg_length))
        return recived_message



    def send(self,message):
        message = str(message)
        msg = message.encode(self.format)
        msg_length = len(msg)
        send_length = str(msg_length).encode(self.format)
        send_length += b' ' * (self.header - len(send_length))
        self.client.send(send_length)
        self.client.send(msg)
        return

    def recive(self):
        msg_length = self.client.recv(self.header).decode(self.format)
        msg_length = int(msg_length)
        msg = self.client.recv(msg_length).decode(self.format)
        return msg

    def disconnect(self):
        self.client.close()



#new_client = Lobby_client(ip="192.168.1.132", port=16000)



