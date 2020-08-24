class Board:

    """
    class Seat:

        def __init__(self, seat_id, x, y):
            self.id = seat_id
            self.cords = (x, y)
            self.state = False

        def sit_down(self, player):
            self.state = player
            self.active_players += 1

        def stand_up(self):
            self.state = False
            self.active_players -= 1
    """

    def __init__(self, game_id, name, min_buy_in, max_buy_in, small_blind):
        self.game_id = game_id
        self.name = name

        self.min_buy_in = min_buy_in
        self.max_buy_in = max_buy_in
        self.small_blind = small_blind
        self.seats = {}

        self.active_players = 0
        self.active_players_ids = []
        self.dealer_pos = 0
        self.hand_id = 0
        self.cards = []

        self.game_status = False
        self.seats_cords = {
            0: [100, 350],
            1: [1238, 350],
            2: [634, 50],
            3: [634, 650]
        }
        for num in range(4):
            x, y = self.seats_cords[num]
            self.seats[num] = Seat(self, num, x, y)

    def start_hand(self):
        self.game_status = True
        self.hand_id += 1
        seats_len = len(self.seats)
        for num in range(1, seats_len + 1):
            if self.seats[(self.dealer_pos + num) % seats_len].state:
                self.dealer_pos = (self.dealer_pos + num) % seats_len
                break
        return Hand(self.hand_id, self.active_players_ids, self.small_blind, self.dealer_pos)

    def count_active_players(self, players):
        self.active_players_ids = []
        for player in players:
            if players[player].seat:
                self.active_players_ids.append(player)


class Seat:

    def __init__(self, master, seat_id, x, y):
        self.master = master
        self.id = seat_id
        self.cords = (x, y)
        self.state = False

    def sit_down(self, player):
        self.state = player
        self.master.active_players += 1

    def stand_up(self):
        self.state = False
        self.master.active_players -= 1


class Hand:

    def __init__(self, hand_id, players, small_blind, dealer_pos):
        self.hand_id = hand_id
        self.small_blind = small_blind
        self.big_blind = small_blind * 2
        self.players = players
        self.dealer_position = dealer_pos
