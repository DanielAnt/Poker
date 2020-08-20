class Board():

    def __init__(self):
        self.ActivePlayers = 0
        self.AvaiablePlaces = 4
        self.slots = {}
        self.cards = []
        for slot in range(self.AvaiablePlaces):
            self.slots[slot] = None


    def player_sit(self,slot,player):
        self.slots[slot] = player
        self.ActivePlayers += 1


    def player_standup(self,slot):
        self.slots[slot] = None
        self.ActivePlayers -= 1






