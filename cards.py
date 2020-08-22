import random

class Cards():


    def __init__(self):
        colors = [
            "H",
            "D",
            "S",
            "C"
        ]
        figurs = [
            "A",
            "K",
            "Q",
            "J",
            "T",
            "9",
            "8",
            "7",
            "6",
            "5",
            "4",
            "3",
            "2"
        ]

        self.deck = []
        for figur in figurs:
            for color in colors:
                self.deck.append(figur+color)

    def  schuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()




