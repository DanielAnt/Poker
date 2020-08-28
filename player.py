class Player():

    def __init__(self, player_id, name="ANDY", money = 0):
        self.name = name
        self.id = player_id
        self.money = money
        self.cards = []
        self.active = False
        self.seat = False

    def get_card(self,card):
        self.cards.append(card)


    def clear_hand(self):
        self.cards = []

    def sit_down(self,seat):
        self.seat = seat

    def stand_up(self):
        if self.seat:
            self.seat.stand_up(self)
            self.seat = False


