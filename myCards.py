from myMath import *
from mySprite import Number,Color
from random import shuffle


class Card:
    def __init__(self, color, number):
        self.color_ = color
        self.number_ = number

    def __repr__(self):
        return "{} {}".format(self.color_, self.number_)


class Deck:
    def __init__(self):
        self.cards_ = []
        self.ncards_ = 108
        self.generateDeck()
        self.shuffle()
        for i in range(7):
            print(self.cards_[i])

    def generateCards(self, color, number, repetition):
        # generate "repetition" cards with "number" and "color"
        for i in range(repetition):
            self.cards_.append(Card(color, number))

    def generateDeck(self):
        l3of = [Number.ONE, Number.THREE, Number.FOUR, Number.FIVE, Number.TWO]
        l2of = [Number.SIX, Number.SEVEN, Number.EIGHT, Number.NINE,
                Number.TEN, Number.JOKER]

        for col in list(Color):
            for n in l3of:
                self.generateCards(col, n, 3)
            for n in l2of:
                self.generateCards(col, n, 2)

    def shuffle(self):
        shuffle(self.cards_)

    def takeTopCard(self):
        self.ncards_ -= 1
        return self.cards_.pop()
