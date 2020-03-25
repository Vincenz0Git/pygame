from Game.cst import Bonus


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


class Play:
    def __init__(self, inHand=[], inBoard=None):
        # inHand: list of Cards
        # inBoard Card
        self.inHand_ = inHand
        self.inBoard_ = inBoard

    def set(self, inHand, inBoard):
        self.inHand_ = inHand
        self.inBoard_ = inBoard

    def noPlay(self):
        return not self.inHand_

    def isRight(self):
        # Play is right if no card is played, one hand card is the same
        # as the one on the board, or two hand cards sum to the one on
        # the board
        if self.inBoard_ and len(self.inHand_) == 0:
            return True
        if len(self.inHand_) == 1:
            return self.inHand_[0].value() == self.inBoard_.value()
        elif len(self.inHand_) == 2:
            return self.inHand_[0].value() + self.inHand_[1].value() == self.inBoard_.value()
        else:
            return False

    def getBonus(self):
        color = self.inBoard_.color()
        if len(self.inHand_) == 1:
            if self.inHand_[0].color() == color:
                return Bonus.COLOR1
        elif len(self.inHand_) == 2:
            if self.inHand_[0].color() == self.inHand_[1].color() == color:
                return Bonus.COLOR2
        else:
            return Bonus.NONE

    def __repr__(self):
        return str(self.inHand_) + "->" + str(self.inBoard_)
