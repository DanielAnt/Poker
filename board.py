from cardlogic2 import *
import time
from _thread import *


class Board:

    def __init__(self, min_buy_in, max_buy_in, small_blind):

        # BOARD SETTINGS
        self.min_buy_in = min_buy_in
        self.max_buy_in = max_buy_in
        self.small_blind = small_blind
        self.hand_id = 0

        # IN GAME STATUS
        self.seating_players = 0
        self.dealer_pos = 1
        self.seats = {}
        self.board_player_money = {}
        self.players_status = {}
        self.cards = []
        self.post_game = False
        self.prize = {}
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

    def sit_down(self, player, buy_in=None):
        if not buy_in:
            buy_in = self.master.min_buy_in
        player_attributes = {
            "id": player.id,
            "name": player.name,
        }
        self.state = player_attributes
        self.master.board_player_money[self.id] = buy_in
        player.money -= buy_in
        self.master.seating_players += 1

    def stand_up(self, player):
        player.money += self.master.board_player_money[self.id]
        del self.master.board_player_money[self.id]
        self.state = False
        self.master.seating_players -= 1


class Hand:

    def __init__(self, master, gameserver, players, cards):

        # GETTING ACCESS TO OTHER CLASSES
        self.master = master
        self.gameserver = gameserver
        self.cards = cards
        self.players = players

        # HAND SETTINGS
        self.hand_id = self.master.hand_id
        self.small_blind = self.master.small_blind
        self.big_blind = self.small_blind * 2

        # INIT VARIABLES
        self.last_player = None
        self.all_in_players = []
        self.all_in_players_subpot = {}
        self.pot_stages = {
            0: 0
        }
        self.subpot_players = []
        self.handed_out_pot = 0
        self.players_cards = {}
        self.players_score = {}

        # INIT BOARD VARIABLES
        self.master.pot = 0
        self.master.check_size = 0
        self.master.game_status = True
        self.master.moving_player_seat_id = None

        seats_len = len(self.master.seats)

        # MOVES DEALER TO NEXT PLAYER
        for num in range(1, seats_len + 1):
            if self.master.seats[(self.master.dealer_pos + num) % seats_len].state:
                self.master.dealer_pos = (self.master.dealer_pos + num) % seats_len
                break

        # MAKING DICT WITH PLAYERS TAKING PART OF GIVEN HAND IN SEATS ORDER
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

        # STARTING HAND, TAKING BLINDS, DEPENDING ON PLAYER NUMBER
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

        # DEALING CARDS, STARTING WITH PLAYER AFTER DEALER
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
        cash = round(float(cash), 1)
        print(cash, self.master.pot)
        if self.master.board_player_money[player.seat.id] > cash:
            self.master.board_player_money[player.seat.id] = round(self.master.board_player_money[player.seat.id]\
                                                             - cash, 1)
            self.master.players_pots[player.id] = round(self.master.players_pots[player.id] + cash, 1)
        else:
            self.master.players_pots[player.id] += round(self.master.board_player_money[player.seat.id], 1)
            self.master.board_player_money[player.seat.id] = 0
            self.all_in_players.append(player.seat.id)
        if self.master.players_pots[player.id] > self.master.check_size:
            self.master.check_size = round(self.master.players_pots[player.id], 1)
            self.last_player = self.current_pos
        self.next_player()

    # GOES TO NEXT STAGE OF THE GAME
    def next_stage(self):
        self.handle_subpots()
        for player_id in self.master.players_pots:
            if self.master.players_pots[player_id]:
                self.master.pot = round(self.master.pot + self.master.players_pots[player_id], 1)
        self.pot_stages[len(self.pot_stages)] = self.master.pot
        self.reset_pots()
        self.last_player = None
        self.dealing_cards()

    # SUMS MAIN POT
    def reset_pots(self):
        self.master.check_size = 0
        self.master.players_pots = {}
        for pos, player in self.players_dict.items():
            if player:
                self.master.players_pots[player.id] = 0

    # SAVES VALUE OF SUB POT IF PLAYER WENT ALL IN
    def handle_subpots(self):
        if len(self.all_in_players) > 0:
            for player_seat in self.all_in_players:
                if player_seat not in self.all_in_players_subpot:
                    bet_size = self.master.players_pots[self.players_dict[player_seat].id]
                    last_pot_size = self.pot_stages[max(self.pot_stages.keys())]
                    self.all_in_players_subpot[player_seat] = last_pot_size
                    for player_id, pot_size in self.master.players_pots.items():
                        if pot_size <= bet_size:
                            self.all_in_players_subpot[player_seat] += pot_size
                        else:
                            self.all_in_players_subpot[player_seat] += bet_size
    # DEALING CARDS TO BOARD
    def dealing_cards(self):
        if self.active_players > 1:
            if self.active_players - len(self.all_in_players) > 1:
                if len(self.master.cards) == 0:
                    for _ in range(3):
                        self.master.cards.append(self.cards.deal_card())
                    self.reset_position()
                elif 5 > len(self.master.cards) >= 3:
                    self.master.cards.append(self.cards.deal_card())
                    self.reset_position()
                elif len(self.master.cards) == 5:
                    start_new_thread(self.end_hand, ())
            else:
                while len(self.master.cards) < 5:
                    self.master.cards.append(self.cards.deal_card())
                start_new_thread(self.end_hand, ())
        else:
            start_new_thread(self.end_hand, ())

    # SETS MOVE_ID TO FIRST ACTIVE PLAYER AFTER DEALER
    def reset_position(self):
        self.current_pos = self.master.dealer_pos
        self.next_player()
        self.last_player = self.current_pos

    # ENDS HAND
    def end_hand(self):
        self.handle_subpots()
        if len(self.all_in_players_subpot) == 0:
            winners = self.find_winner()
            self.split_pot(winners, self.master.pot)
        else:
            for pos, pot in sorted(self.all_in_players_subpot.items(), key=lambda item: item[1]):
                if self.master.pot > 0:
                    pot -= self.handed_out_pot
                    winners = self.find_winner(pos)
                    self.master.pot -= pot
                    self.split_pot(winners, pot)
            if self.master.pot > 0:
                winners = self.find_winner()
                self.split_pot(winners, self.master.pot)

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

    # END GAME FUNCTIONS
    def find_winner(self, subpot_winner=None):
        self.players_score = {}
        self.players_cards = {}
        if self.active_players > 1:
            for pos, player in self.players_dict.items():
                if player:
                    if self.master.players_status[pos] and pos not in self.subpot_players:
                        self.players_cards[pos] = PokerHand(pos, player.cards, self.master.cards)
                        self.players_score[pos] = self.players_cards[pos].score

            winning_player = min(self.players_score, key=self.players_score.get)
            winning_score = self.players_score[winning_player]
            winners = []
            for pos, score in self.players_score.items():
                if winning_score == score:
                    winners.append(pos)
        else:
            winners = []
            for pos, status in self.master.players_status.items():
                if status:
                    winners.append(pos)
        if subpot_winner:
            self.subpot_players.append(subpot_winner)
        return winners

    def split_pot(self, winners, pot):
        print(f'player {winners}, won {pot}')
        self.handed_out_pot += round(pot, 1)
        if len(winners) > 1:
            split_pot = pot / len(winners)
            split_pot = round(split_pot, 1)
            for winner in winners:
                self.master.board_player_money[winner] += split_pot
                if winner not in self.master.prize:
                    self.master.prize[winner] = 0
                self.master.prize[winner] += split_pot
        else:
            self.master.board_player_money[winners[0]] += round(pot, 1)
            if winners[0] not in self.master.prize:
                self.master.prize[winners[0]] = 0
            self.master.prize[winners[0]] += round(pot, 1)

    # INIT SHOWDOWN
    def post_game(self):
        self.master.post_game = True
        for pos, player in self.players_dict.items():
            if player and self.master.players_status[pos]:
                self.master.players_post_game_cards[pos] = player.cards
        time.sleep(5)
        self.master.post_game = False
        self.master.players_post_game_cards = {}
        self.master.prize = {}
