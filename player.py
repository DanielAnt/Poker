class Player():

    def __init__(self,name="ANDY", money = 0):
        self.name = name
        self.money = money
        self.cards = []
        self.seat = False

    def get_card(self,card):
        self.cards.append(card)


    def clear_hand(self):
        self.cards = []

    def sit_down(self,seat):
        self.seat = seat

    def stand_up(self):
        self.seat.stand_up()
        self.seat = False


