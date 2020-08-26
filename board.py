class Board:

    def __init__(self, game_id, name, min_buy_in, max_buy_in, small_blind):
        self.game_id = game_id
        self.name = name

        self.min_buy_in = min_buy_in
        self.max_buy_in = max_buy_in
        self.small_blind = small_blind
        self.seats = {}

        self.active_players = 0
        self.active_players_ids = []
        self.dealer_pos = 1
        self.hand_id = 0
        self.cards = []
        self.pot = None
        self.players_pots = None

        self.game_status = False
        for num in range(8):
            self.seats[num] = Seat(self, num)

    def start_hand(self, players):
        self.game_status = True
        self.hand_id += 1
        seats_len = len(self.seats)
        for num in range(1, seats_len + 1):
            if self.seats[(self.dealer_pos + num) % seats_len].state:
                self.dealer_pos = (self.dealer_pos + num) % seats_len
                break
        return Hand(self.hand_id, players, self.small_blind, self.dealer_pos, self.seats)


class Seat:

    def __init__(self, master, seat_id):
        self.master = master
        self.id = seat_id
        self.state = False

    def sit_down(self, player):
        player_attributes = {
            "id": player.id,
            "name": player.name,
            "money": player.money
        }
        self.state = player_attributes
        self.master.active_players += 1

    def stand_up(self):
        self.state = False
        self.master.active_players -= 1


class Hand:

    def __init__(self, hand_id, players, small_blind, dealer_pos, seats):
        self.hand_id = hand_id
        self.small_blind = small_blind
        self.big_blind = small_blind * 2
        self.active_players = self.count_active_players(players)
        self.active_seats = self.count_active_seats(seats)
        self.orderd_player_list = []
        self.pot = 0
        for pos, seat in enumerate(self.active_seats):
            if seat.id == dealer_pos:
                self.dealer_position = pos
            for player in self.active_players:
                if seat.state["id"] == player.id:
                    self.orderd_player_list.append(player)
        self.current_pos = self.dealer_position
        self.reset_pots()

        if len(self.active_players) == 2:
            self.put_players_money_to_pot(self.orderd_player_list[self.current_pos],
                                          self.small_blind)
            self.next_player()
            self.put_players_money_to_pot(self.orderd_player_list[self.current_pos],
                                          self.big_blind)
            self.next_player()
        else:
            self.next_player()
            self.put_players_money_to_pot(self.orderd_player_list[self.current_pos],
                                          self.small_blind)
            self.next_player()
            self.put_players_money_to_pot(self.orderd_player_list[self.current_pos],
                                          self.big_blind)
            self.next_player()

    def count_active_players(self, players):
        return [players[player] for player in players if players[player].seat]

    def count_active_seats(self, seats):
        return [seats[seat] for seat in seats if seats[seat].state]

    def next_player(self):
        self.current_pos = (self.current_pos + 1) % len(self.active_players)

    def put_players_money_to_pot(self, player, cash):
        if player.money >= cash:
            player.money = player.money - cash
            self.players_pots[player.id] += cash
            self.pot += cash

        else:
            self.players_pots[player.id] += player.money
            self.pot += player.money
            player.money = 0

    def reset_pots(self):
        self.players_pots = {}
        for player in self.orderd_player_list:
            self.players_pots[player.id] = 0

    def return_pots(self):
        return self.pot, self.players_pots
