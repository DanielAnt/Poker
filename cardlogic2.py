#from pokereval.card import Card
from pokereval.hand_evaluator import HandEvaluator
from treys import Deck
from treys import Card
from treys import Evaluator




class PokerHand(object):

    def __init__(self, pos, hand, board):
        self.hand = self.translate(hand)
        self.board = self.translate(board)
        self.pos = pos
        print(f'player{pos} has {Card.print_pretty_cards(self.board+self.hand)}')
        self.evaluator = Evaluator()
        self.score = self.evaluator.evaluate(self.board, self.hand)
        self.score_class = self.evaluator.get_rank_class(self.score)
        print(self.evaluator.class_to_string(self.score_class))

    def translate(self, cards):
        colors = {
            "S": 's',
            "H": 'h',
            "D": 'd',
            "C": 'c'
        }
        hand = []
        for card in cards:
            hand.append(Card.new(card[0] + colors[card[1]]))
        return hand


if __name__ == '__main__':

    hand1 = ["AS", "AD"]
    hand2 = ["AH", "QD"]
    hand3 = ["9S", "2S"]
    board = ["TS", "KS",'QS',"JS", "5D"]

    p1 = PokerHand(1, hand1, board)
    p2 = PokerHand(2, hand2, board)
    p3 = PokerHand(3, hand3, board)

    print(f'p1 = {p1.score}, p2 = {p2.score}, p3 = {p3.score} ')
    print(f'p1 = {p1.score_class}, p2 = {p2.score_class}, p3 = {p3.score_class} ')
    print("Player %d hand rank = %d (%s)\n" % (p1.pos ,p1.score, p1.evaluator.class_to_string(p1.score_class)))
