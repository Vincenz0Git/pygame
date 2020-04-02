from Game.myCards import Hand
from Game.cst import Bonus
from Game.gameMechanics import Play

class Player:
    def __init__(self):
        self.hand_ = Hand()
        self.plays_ = []
        self.bonus_ = []
        self.lastPlay_ = ()

    def deal1(self, deck):
        self.hand_.add(deck.takeTop())

    def dealn(self, deck, n):
        for _ in range(n):
            self.deal1(deck)

    def getCard(self, n):
        # get the nth card of the hand and remove it
        return self.hand_.pop(n)

    def addPlay(self, cardFromHand, cardInBoard):
        alreadyOnBoard = False
        for play in self.plays_:
            if play.inBoard_ == cardInBoard:
                alreadyOnBoard = True
                play.add(cardFromHand)
                self.lastPlay_ = (cardFromHand, cardInBoard)
        if not self.plays_ or not alreadyOnBoard:
            self.plays_.append(Play([cardFromHand], cardInBoard))
            self.lastPlay_ = (cardFromHand, cardInBoard)

    def allPlaysRight(self):
        allRight = True
        for play in self.plays_:
            if not play.isRight():
                allRight = False
                break
        return allRight

    def getBonus(self):
        for play in self.plays_:
            if len(play) == 1:
                if play[0].color_ == play.inBoard_.color_:
                    self.bonus_.append(Bonus.COLOR1)
            if len(play) == 2:
                if play[0].color_ == play[1].color_ == play.inBoard_.color_:
                    self.bonus_.append(Bonus.COLOR2)

    def getLastPlay(self):
        for play in self.plays_:
            if play.inBoard_ == self.lastPlay_[1]:
                play.takebyid(self.lastPlay_[0].uuid_)
                return self.lastPlay_

    def takeCardbyid(self, id):
        return self.hand_.takebyid(id)

    def setPlay(self, iplay, play):
        self.plays_[iplay] = play

    def __repr__(self):

        return self.hand_.__repr__() +'\n'+'\n'.join([str(play) for play in self.plays_])

    def __getitem__(self, item):
        return self.hand_[item]
