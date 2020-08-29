from cardlogic2 import *
import time
from _thread import *

class Board:

    def __init__(self, game_id, name, min_buy_in, max_buy_in, small_blind):
        self.game_id = game_id
        self.name = name
        self.connected_players = []
        self.min_buy_in = min_buy_in
        self.max_buy_in = max_buy_in
        self.small_blind = small_blind
        self.seats = {}

        self.active_players = 0
        self.active_players_ids = []
        self.board_player_money = {}
        self.players_status = {}
        self.dealer_pos = 1
        self.hand_id = 0
        self.cards = []
        self.post_game = False
        self.players_post_game_cards = {}
        self.check_size = 0
        self.pot = None
        self.players_pots = {}
        self.moving_player_seat_id = None
        self.game_status = False
        for num in range(8):
            self.seats[num] = Seat(self, num)
            self.players_status[num] = False
            self.players_pots[num] = 0

    def start_hand(self, gameserver, players, cards):
        self.game_status = True
        self.hand_id += 1
        return Hand(self, gameserver, players, cards)


class Seat:

    def __init__(self, master, seat_id):
        self.master = master
        self.id = seat_id
        self.state = False

    def sit_down(self, player):
        player_attributes = {
            "id": player.id,
            "name": player.name,
            "money": player.money,
            "active": player.active
        }
        self.state = player_attributes
        self.master.board_player_money[self.id] = 20
        player.money -= 20
        self.master.active_players += 1

    def stand_up(self, player):
        player.money += self.master.board_player_money[self.id]
        del self.master.board_player_money[self.id]
        self.state = False
        self.master.active_players -= 1


class Hand:

    def __init__(self, master, gameserver, players, cards):
        self.master = master
        self.gameserver = gameserver
        self.cards = cards
        self.players = players
        self.hand_id = self.master.hand_id
        self.small_blind = self.master.small_blind
        self.big_blind = self.small_blind * 2

        self.all_in_players = []
        self.all_in_players_subpot = {}
        self.pot_stages = {
            0 : 0
        }
        self.players_cards = {}
        self.players_score = {}
        self.master.pot = 0
        self.master.check_size = 0
        self.last_player = None
        self.master.game_status = True
        self.master.moving_player_seat_id = None

        seats_len = len(self.master.seats)
        ### moves dealer to next player
        for num in range(1, seats_len + 1):
            if self.master.seats[(self.master.dealer_pos + num) % seats_len].state:
                self.master.dealer_pos = (self.master.dealer_pos + num) % seats_len
                break

        self.players_dict = {}
        for pos, seat in self.master.seats.items():
            if seat.state:
                self.players_dict[pos] = self.players[seat.state["id"]]
                self.master.players_status[pos] = True
            else:
                self.players_dict[pos] = False
                self.master.players_status[pos] = False

        self.active_players = self.count_active_players()

        self.current_pos = self.master.dealer_pos
        self.reset_pots()

        if self.active_players == 2:
            self.put_players_money_to_pot(self.players_dict[self.current_pos],
                                          self.small_blind)

            self.put_players_money_to_pot(self.players_dict[self.current_pos],
                                          self.big_blind)
            self.last_player = self.current_pos
        else:
            self.next_player()
            self.put_players_money_to_pot(self.players_dict[self.current_pos],
                                          self.small_blind)
            self.put_players_money_to_pot(self.players_dict[self.current_pos],
                                          self.big_blind)
            self.last_player = self.current_pos
            self.master.moving_player_seat_id = self.current_pos



        ## DEALING CARDS
        cards_to_deal = self.active_players * 2
        seats_len = len(self.players_dict)
        deal_pos = (self.master.dealer_pos + 1) % seats_len
        i = 0
        k = 0
        while k < cards_to_deal:
            if self.players_dict[deal_pos]:
                self.players_dict[deal_pos].cards.append(self.cards.deal_card())
                k += 1
            deal_pos = (deal_pos + 1) % seats_len
            i += 1



    def count_active_players(self):
        k = 0
        for status in self.master.players_status.values():
            if status:
                k += 1
        return k

    def count_active_seats(self, seats):
        return [seats[seat] for seat in seats if seats[seat].state]

    def next_player(self):
        self.active_players = self.count_active_players()
        if self.active_players > 1:
            while True:
                self.current_pos = (self.current_pos + 1) % len(self.players_dict)
                if self.current_pos == self.last_player:
                    self.next_stage()
                    break
                if self.players_dict[self.current_pos]:
                    if self.master.players_status[self.current_pos] and self.current_pos not in self.all_in_players:
                        self.master.moving_player_seat_id = self.current_pos
                        break
        else:
            self.next_stage()



    def put_players_money_to_pot(self, player, cash):
        cash = float(cash)
        if self.master.board_player_money[player.seat.id] >= cash:
            self.master.board_player_money[player.seat.id] = self.master.board_player_money[player.seat.id]\
                                                             - cash
            self.master.players_pots[player.id] += cash
        else:
            self.master.players_pots[player.id] += self.master.board_player_money[player.seat.id]
            self.master.board_player_money[player.seat.id] = 0
            self.all_in_players.append(player.seat.id)
        if self.master.players_pots[player.id] > self.master.check_size:
            self.master.check_size = self.master.players_pots[player.id]
            self.last_player = self.current_pos
        self.next_player()

    def reset_pots(self):
        self.master.check_size = 0
        self.master.players_pots = {}
        for pos, player in self.players_dict.items():
            if player:
                self.master.players_pots[player.id] = 0

    def return_pots(self):
        return self.master.pot, self.master.players_pots

    def deal_cards(self):
        if len(self.master.cards) == 0:
            for _ in range(3):
                self.master.cards.append(self.cards.deal_card())
        elif 5 > len(self.master.cards) > 2:
            self.master.cards.append(self.cards.deal_card())

    def handle_subpots(self):
        if len(self.all_in_players) > 0:
            for player_seat in self.all_in_players:
                if player_seat not in self.all_in_players_subpot:
                    bet_size = self.master.players_pots[self.players_dict[player_seat]]
                    last_pot_size = self.pot_stages[max(self.pot_stages.keys())]
                    self.all_in_players_subpot[player_seat] = last_pot_size
                    for player_id, pot_size in self.master.players_pots.items():
                        if pot_size <= bet_size:
                            self.all_in_players_subpot[player_seat] += pot_size
                        else:
                            self.all_in_players_subpot[player_seat] += bet_size


    def next_stage(self):
        self.handle_subpots()

        for player_id in self.master.players_pots:
            if self.master.players_pots[player_id]:
                self.master.pot += self.master.players_pots[player_id]
        self.pot_stages[len(self.pot_stages)] = self.master.pot
        self.reset_pots()
        self.last_player = None
        if self.active_players - len(self.all_in_players) > 1:
            self.current_pos = self.master.dealer_pos
            self.next_player()
            self.last_player = self.current_pos
        self.dealing_cards()

    def dealing_cards(self):
        if self.active_players > 1:
            if self.active_players - len(self.all_inplayers) > 1:
                if len(self.master.cards) == 0:
                    for _ in range(3):
                        self.master.cards.append(self.cards.deal_card())
                elif 5 > len(self.master.cards) >= 3:
                    self.master.cards.append(self.cards.deal_card())
                elif len(self.master.cards) == 5:
                    start_new_thread(self.end_hand, ())
            else:
                while len(self.master.cards) < 5:
                    self.master.cards.append(self.cards.deal_card())
                start_new_thread(self.end_hand, ())
        else:
            start_new_thread(self.end_hand, ())



    def find_winner(self):
        self.players_score = {}
        self.players_cards = {}
        if self.active_players > 1:
            for pos, player in self.players_dict.items():
                if player:
                    if self.master.players_status[pos]:
                        self.players_cards[pos] = PokerHand(pos, player.cards, self.master.cards)
                        self.players_score[pos] = self.players_cards[pos].score

            winning_player = min(self.players_score, key=self.players_score.get)
            winning_score = self.players_score[winning_player]
            winners = []
            print(winning_player, winning_score, self.players_score)
            for pos, score in self.players_score.items():
                if winning_score == score:
                    winners.append(pos)
        else:
            winners = []
            for pos, status in self.master.players_status.items():
                if status:
                    winners.append(pos)

        return winners

    def split_pot(self, winners):
        if len(winners) > 1:
            split_pot = self.master.pot / len(winners)
            split_pot = round(split_pot, 1)
            for winner in winners:
                self.master.board_player_money[winner] += split_pot
        else:
            self.master.board_player_money[winners[0]] += round(self.master.pot, 1)

    def post_game(self):
        self.master.post_game = True
        for pos, player in self.players_dict.items():
            if player and self.master.players_status[pos]:
                self.master.players_post_game_cards[pos] = player.cards
        time.sleep(5)
        self.master.post_game = False
        self.master.players_post_game_cards = {}

    def end_hand(self):
        winners = self.find_winner()
        self.split_pot(winners)
        if self.active_players > 1:
            self.post_game()

        for player in self.players_dict.values():
            if player:
                player.cards = []

        self.master.cards = []
        self.reset_pots()
        self.master.game_status = False
        self.master.moving_player_seat_id = None
        self.gameserver.start_hand()




