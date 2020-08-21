class Board():

    class seat():
        


    def __init__(self):
        self.ActivePlayers = 0
        self.AvaiablePlaces = 4
        self.slots = {}
        self.cards = []
        self.slotsCords = {
            0 : [100,350],
            1 : [1238,350],
            2 : [634,50],
            3 : [634,650]
        }

        for slot in range(self.AvaiablePlaces):
            self.slots[slot] = None


    def player_sit(self,slot,player):
        self.slots[slot] = player
        self.ActivePlayers += 1


    def player_standup(self,slot):
        self.slots[slot] = None
        self.ActivePlayers -= 1






