from Game.cst import Bonus
from Game.myCards import Pile

class Engine:
    # Interact with the plays, to check if they follow the rules
    def __init__(self):
        pass

    def checkPlay(self, play):
        if play.isRight():
            return True
        else:
            return False

    def checkBonus(self, play):
        return play.getBonus()


class Play(Pile):
    def __init__(self, inHand=[], inBoard=None, last=False):
        # inHand: list of Cards
        # inBoard Card
        super().__init__()
        for card in inHand:
            self.add(card)
        self.ncards_ = len(inHand)
        self.inBoard_ = inBoard
        self.lastPlay_ = last

    def set(self, inHand, inBoard):
        self.cards_ = inHand
        self.inBoard_ = inBoard

    def noPlay(self):
        return not self.cards_

    def isRight(self):
        # Play is right if no card is played, one hand card is the same
        # as the one on the board, or two hand cards sum to the one on
        # the board
        if self.inBoard_ and len(self.cards_) == 0:
            return True
        if len(self.cards_) == 1:
            return self.cards_[0].value() == self.inBoard_.value()
        elif len(self.cards_) == 2:
            return self.cards_[0].value() + self.cards_[1].value() == self.inBoard_.value()
        else:
            return False

    def getBonus(self):
        color = self.inBoard_.color()
        if len(self.cards_) == 1:
            if self.cards_[0].color() == color:
                return Bonus.COLOR1
        elif len(self.cards_) == 2:
            if self.cards_[0].color() == self.cards_[1].color() == color:
                return Bonus.COLOR2
        else:
            return Bonus.NONE

    def __repr__(self):
        return str(self.cards_) + "->" + str(self.inBoard_)
