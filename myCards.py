from myMath import *
from mySprite import Number,Color
from random import shuffle


class Card:
    def __init__(self, color, number):
        self.color_ = color
        self.number_ = number

    def __eq__(self, autre):
        return self.number_ == autre.number_

    def __add__(self, autre):
        return

    def __repr__(self):
        return self.color_.name[0] + str(self.number_.value)
        #return "{} {}".format(self.color_, self.number_)


class Pile:
    def __init__(self):
        self.cards_ = []
        self.ncards_ = 0

    def __repr__(self):
        return "{}".format(self.ncards_)


class Center(Pile):
    def __init__(self):
        Pile.__init__(self)

    def new(self, deck, n):
        self.ncards_ = n
        for _ in range(n):
            self.cards_.append(deck.takeTopCard())

    def __repr__(self):
        return "(Center "+Pile.__repr__(self)+' '+' '.join([str(el) for el in self.cards_])+")"


class Discards(Pile):
    def __init__(self):
        Pile.__init__(self)

    def __repr__(self):
        return "(Discards "+Pile.__repr__(self)+")"


class Deck(Pile):
    def __init__(self):
        Pile.__init__(self)
        self.new()
        self.shuffle()
        # for i in range(7):
        #     print(self.cards_[i])

    def generateCards(self, color, number, repetition):
        # generate "repetition" cards with "number" and "color"
        for i in range(repetition):
            self.cards_.append(Card(color, number))

    def new(self):
        # Create fresh deck of cards with given set of cards given by
        # the rules
        self.ncards_ = 108
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

    def __repr__(self):
        return "(Deck "+Pile.__repr__(self)+")"
