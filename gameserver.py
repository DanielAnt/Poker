import socket
from board import *
from player import *
from cards import *
import pickle


class GameServer:

    def __init__(self, name, ip, port, gameid, min_buy_in, max_buy_in, blind):
        self.board = Board(min_buy_in, max_buy_in, blind)
        self.game_id = gameid
        self.name = name
        self.ip = ip
        self.port = port
        self.connected_players = []
        self.addr = (self.ip, self.port)
        self.format = "utf-8"
        self.header = 512
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.addr)
        self.players = {}
        self.hand = None
        print(f'Name={self.name} IP={self.ip} PORT={self.port} has started GAME SERVER')
        self.connect_players()

    # SERVER HANDLING
    def connect_players(self):
        self.server.listen(4)
        while True:
            conn, addr = self.server.accept()
            print(addr, " has connected to game server")
            start_new_thread(self.authentication, (conn,))

    def recive_message(self, user):
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
                    if player_id in self.connected_players:
                        self.send_pickle(user, message=False)
                        break
                    else:
                        login_client = True
                        if player_id not in self.players:
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
        self.connected_players.append(player_id)
        while connected:
            try:
                msg_length = user.recv(self.header).decode(self.format)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = user.recv(msg_length).decode(self.format)
                    if msg == "UPDATE":
                        self.send_pickle(user, [self.board, self.players[player_id]])

                    elif msg == "BET":
                        bet_size = self.recive_message(user)
                        if self.board.moving_player_seat_id == self.players[player_id].seat.id:
                            if float(bet_size) >= self.board.check_size - self.board.players_pots[player_id]:
                                self.hand.put_players_money_to_pot(self.players[player_id], bet_size)

                    elif msg == "CHECK":
                        self.game_check(player_id)

                    elif msg == "PASS":
                        self.game_pass(player_id)

                    elif msg == "START":
                        self.start_hand()

                    elif msg == "SIT":
                        message = self.recive_message(user)
                        seat_id, buy_in_size = message.split(";")
                        seat_id = int(seat_id)
                        buy_in_size = float(buy_in_size)
                        if not self.board.seats[seat_id].state and not self.players[player_id].seat:
                            self.board.seats[seat_id].sit_down(self.players[player_id], buy_in_size)
                            self.players[player_id].sit_down(self.board.seats[seat_id])

                    elif msg == "SEATBACK":
                        self.players[player_id].stand_up_queue = False

                    elif msg == "STANDUP":
                        self.game_standup(player_id)

                    elif msg == "bye":
                        connected = False
                else:
                    connected = False
            except Exception as e:
                print(e)
                break

        user.close()
        print(f"{player_id} has disconnected")

        if self.players[player_id].seat:
            self.game_standup(player_id)

        self.connected_players.remove(player_id)
        if self.players[player_id].seat.id == self.board.moving_player_seat_id:
            time.sleep(30)
            if player_id not in self.connected_players:
                self.game_pass(player_id)


    # GAME HANDLING
    def start_hand(self):
        for player in self.players.values():
            if player.seat:
                if self.board.board_player_money[player.seat.id] == 0:
                    player.stand_up()
        for player in self.players.values():
            if player.stand_up_queue:
                player.stand_up()

        if self.board.seating_players > 1 and not self.board.game_status:
            self.cards = Cards()
            self.cards.schuffle()
            self.hand = self.board.start_hand(self, self.players, self.cards)

    def game_check(self, player_id):
        if self.board.moving_player_seat_id == self.players[player_id].seat.id:
            if self.board.board_player_money[self.players[player_id].seat.id] >= \
                    self.board.check_size - self.board.players_pots[player_id]:
                bet = round(float(self.board.check_size - self.board.players_pots[player_id]), 1)
                self.hand.put_players_money_to_pot(self.players[player_id], bet)
            else:
                if self.board.board_player_money[self.players[player_id].seat.id] > 0:
                    self.hand.put_players_money_to_pot(self.players[player_id],
                                                       self.board.board_player_money
                                                       [self.players[player_id].seat.id])

    def game_pass(self, player_id):
        if self.board.moving_player_seat_id == self.players[player_id].seat.id:
            if self.board.check_size == self.board.players_pots[player_id]:
                self.hand.next_player()
            else:
                self.board.players_status[self.players[player_id].seat.id] = False
                self.hand.next_player()

    def game_standup(self,player_id):
        if self.board.players_status[self.players[player_id].seat.id]:
            self.players[player_id].stand_up_queue = True
        else:
            self.players[player_id].stand_up()


if __name__ == '__main__':

    GameServer("test", "192.168.1.132", 16001, 10000, 20, 40, 2)
