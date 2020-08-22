class Board:

    class Seat:

        def __init__(self, x, y):
            self.cords = (x, y)
            self.state = False

        def sit_down(self, player):
            self.state = player

        def stand_up(self):
            self.state = False

    def __init__(self, game_id, name, min_buy_in, max_buy_in, small_blind):
        self.game_id = game_id
        self.name = name
        self.min_buy_in = min_buy_in
        self.max_buy_in = max_buy_in
        self.small_blind = small_blind
        self.seats = {}
        self.seats_cords = {
            0: [100, 350],
            1: [1238, 350],
            2: [634, 50],
            3: [634, 650]
        }
        for num in range(4):
            x, y = self.seats_cords[num]
            self.seats[num] = self.Seat(x, y)
