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
        self.moving_player_seat_id = None

        self.game_status = False
        for num in range(8):
            self.seats[num] = Seat(self, num)

    def start_hand(self, players, cards):
        self.game_status = True
        self.hand_id += 1
        return Hand(self, players, cards)


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
        self.master.active_players += 1

    def stand_up(self):
        self.state = False
        self.master.active_players -= 1


class Hand:

    def __init__(self, master, players, cards):
        self.master = master
        self.cards = cards
        self.hand_id = self.master.hand_id
        self.small_blind = self.master.small_blind
        self.big_blind = self.small_blind * 2
        self.active_players = self.count_active_players(players)
        self.active_seats = self.count_active_seats(self.master.seats)
        self.orderd_player_list = []
        self.pot = 0
        self.check_size = 0
        self.last_player = None

        seats_len = len(self.master.seats)
        for num in range(1, seats_len + 1):
            if self.master.seats[(self.master.dealer_pos + num) % seats_len].state:
                self.master.dealer_pos = (self.master.dealer_pos + num) % seats_len
                break

        for pos, seat in enumerate(self.active_seats):
            if seat.id == self.master.dealer_pos:
              self.master.dealer_position = pos
            for player in self.active_players:
                if seat.state["id"] == player.id:
                    self.orderd_player_list.append(player)
                    player.active = True

        self.current_pos = self.master.dealer_position
        self.reset_pots()

        if len(self.active_players) == 2:
            self.put_players_money_to_pot(self.orderd_player_list[self.current_pos],
                                          self.small_blind)
            self.next_player()
            last_player = self.current_pos
            self.put_players_money_to_pot(self.orderd_player_list[self.current_pos],
                                          self.big_blind)
            self.next_player()
            self.last_player = last_player
        else:
            self.next_player()
            self.put_players_money_to_pot(self.orderd_player_list[self.current_pos],
                                          self.small_blind)
            self.next_player()
            last_player = self.current_pos
            self.put_players_money_to_pot(self.orderd_player_list[self.current_pos],
                                          self.big_blind)
            self.next_player()
            self.last_player = last_player

        deal_pos = self.master.dealer_position + 1
        number_of_players = len(self.orderd_player_list)
        i = 0
        while i < 2 * number_of_players:
            self.orderd_player_list[deal_pos].cards.append(self.cards.deal_card())
            deal_pos = (deal_pos + 1) % number_of_players
            i += 1





    def count_active_players(self, players):
        return [players[player] for player in players if players[player].seat]

    def count_active_seats(self, seats):
        return [seats[seat] for seat in seats if seats[seat].state]

    def next_player(self):
        while True:
            self.current_pos = (self.current_pos + 1) % len(self.active_players)
            if self.current_pos == self.last_player:
                self.next_stage()
            if self.orderd_player_list[self.current_pos].active:
                break
        self.master.moving_player_seat_id = self.orderd_player_list[self.current_pos].seat.id


    def put_players_money_to_pot(self, player, cash):
        cash = float(cash)
        if player.money >= cash:
            player.money = player.money - cash
            self.players_pots[player.id] += cash
            self.pot += cash
        else:
            self.players_pots[player.id] += player.money
            self.pot += player.money
            player.money = 0
        if self.players_pots[player.id] > self.check_size:
            self.check_size = self.players_pots[player.id]
            self.last_player = self.current_pos

    def reset_pots(self):
        self.players_pots = {}
        for player in self.orderd_player_list:
            self.players_pots[player.id] = 0

    def return_pots(self):
        return self.pot, self.players_pots

    def deal_cards(self):
        if len(self.master.cards) == 0:
            for _ in range(3):
                self.master.cards.append(self.cards.deal_card())
        elif 5 > len(self.master.cards) > 2:
            self.master.cards.append(self.cards.deal_card())


    def next_stage(self):
        for player_id in self.players_pots:
            self.pot += self.players_pots[player_id]
        self.reset_pots()
        self.last_player = None
        self.current_pos = self.master.dealer_pos
        self.next_player()
        self.last_player = self.master.dealer_pos
        self.dealing_cards()

    def dealing_cards(self):
        if len(self.master.cards) == 0:
            for _ in range(3):
                self.master.cards.append(self.cards.deal_card())
        elif 5 > len(self.master.cards) >= 3:
            self.master.cards.append(self.cards.deal_card())
        elif len(self.master.cards) > 5:
            print("THE WINNER IS")