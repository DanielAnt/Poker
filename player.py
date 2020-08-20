class Player():

    def __init__(self,money = 0, name = "BOT"):
        self.status = "Inactive"
        self.name = name
        self.money = money
        self.cards = []

    def get_card(self,card):
        self.cards.append(card)


    def clear_hand(self):
        self.cards = []

