import socket
from _thread import *
from board import *
from player import *
from cards import *
import pickle

class GameServer:

    def __init__(self, name, ip, port, gameid, min_buy_in, max_buy_in, blind):
        self.board = Board(gameid, name, min_buy_in, max_buy_in, blind)
        self.name = name
        self.ip = ip
        self.port = port
        self.addr = (self.ip, self.port)
        self.format = "utf-8"
        self.header = 512
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.addr)
        self.players = {}
        print(f'Name={self.name} IP={self.ip} PORT={self.port} has started GAME SERVER')
        self.connect_players()

    def recive_message(self,user):
        msg_length = user.recv(self.header).decode(self.format)
        msg_length = int(msg_length)
        return user.recv(msg_length).decode(self.format)

    def send_message(self, user, message):
        msg = message.encode(self.format)
        msg_length = len(msg)
        message_header = str(msg_length).encode(self.format)
        message_header += b' ' * (self.header - len(message_header))
        user.send(message_header)
        user.send(msg)

    def send_pickle(self, user, message):
        msg = pickle.dumps(message)
        msg_length = len(msg)
        send_length = str(msg_length).encode(self.format)
        send_length += b' ' * (self.header - len(send_length))
        user.send(send_length)
        user.send(msg)

    def authentication(self, user):
        login_client = False
        user.settimeout(5)
        while True:

            msg_length = user.recv(self.header).decode(self.format)
            if msg_length:
                msg_length = int(msg_length)
                msg = user.recv(msg_length).decode(self.format)
                if msg == "LOGIN":
                    player_info = self.recive_message(user)
                    player_id, player_name = player_info.split(";")
                    if player_id in self.players:
                        self.send_pickle(user, message=False)
                        break
                    else:
                        login_client = True
                        self.players[player_id] = Player(player_id, player_name, 100)
                        self.send_pickle(user, self.players[player_id])
                        break
            else:
                print("timeout")
        if login_client:
            self.connect_client(user, player_id)
        else:
            print(f'{user} disconnected')
            user.close()


    def connect_client(self, user, player_id):
        connected = True
        while connected:
            try:
                msg_length = user.recv(self.header).decode(self.format)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = user.recv(msg_length).decode(self.format)
                    if msg == "UPDATE":
                        self.send_pickle(user, [self.board, self.players[player_id]])
                    elif msg == "LOGIN":
                        player_info = self.recive_message(user)
                        player_id, player_name = player_info.split(";")
                        self.players[player_id] = Player(player_id, player_name, 100)
                        self.send_pickle(user, self.players[player_id])
                    elif msg == "START":
                        if self.board.active_players > 1 and not self.board.game_status:
                            hand = self.board.start_hand(self.players)
                            self.cards = Cards()
                            self.cards.schuffle()
                            for _ in range(2):
                                for player in self.players:
                                    if self.players[player].seat:
                                        self.players[player].cards.append(self.cards.deal_card())
                    elif msg == "DEALCARDS":
                        if len(self.board.cards) == 0:
                            for _ in range(3):
                                self.board.cards.append(self.cards.deal_card())
                        elif 5 > len(self.board.cards) > 2:
                                self.board.cards.append(self.cards.deal_card())



                    elif msg == "SIT":
                        seat_id = self.recive_message(user)
                        seat_id = int(seat_id)
                        if self.board.seats[seat_id].state == False and self.players[player_id].seat == False:
                            self.board.seats[seat_id].sit_down(self.players[player_id])
                            self.players[player_id].sit_down(self.board.seats[seat_id])
                    elif msg == "STANDUP":
                        self.players[player_id].stand_up()
                    elif msg == "bye":
                        connected = False
                else:
                    connected = False
            except Exception as e:
                print(e)
                break
        print(f"{player_id} has disconnected")
        if self.players[player_id].seat:
            self.players[player_id].stand_up()
        del self.players[player_id]
        if self.board.active_players < 2:
            self.board.game_status = False
        user.close()


    def connect_players(self):
        self.server.listen(4)
        while True:
            conn, addr = self.server.accept()
            print(addr, " has connected to game server")
            start_new_thread(self.authentication, (conn,))

if __name__ == '__main__':

    GameServer("test", "192.168.1.132", 16001, 10000, 100, 200, 2)

