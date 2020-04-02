from Game.myMath import *
from Game.cst import Number, Color
from random import shuffle
import csv


class Card:
    # TODO definitely add uuid
    def __init__(self, color, number, id=None):
        self.uuid_ = id
        self.color_ = color
        self.number_ = number
        self.joker_ = None

    def value(self, joker=None):
        if not joker:
            return self.number_.value
        else:
            return joker

    def repruid(self):
        return '(' + str(self.uuid_) + ')'

    def color(self):
        return self.color_.name

    def __eq__(self, autre):
        return self.number_ == autre.number_

    def __repr__(self):
        if self.joker_ == 'number':
            if self.number_ == Number.JOKER:
                return self.color_.name[0] + 'J' + self.repruid()
            else:
                return self.color_.name[0] + 'J' + ':' + str(self.number_.value) + ':' + self.repruid()
        elif self.joker_ == 'color':
            if self.color_ == Color.JOKER:
                return 'J' + str(self.number_.value) + self.repruid()
            else:
                return 'J'+ ':' + self.color_.name[0] + ':' + str(self.number_.value) + self.repruid()
        else:
            return self.color_.name[0] + str(self.number_.value) + self.repruid()
        #return "{} {}".format(self.color_, self.number_)


class Pile:
    # Collection of card, useful methods to add and remove keeping the count
    def __init__(self):
        self.cards_ = []
        self.ncards_ = 0

    def add(self, card):
        self.ncards_ += 1
        self.cards_.append(card)

    def getn(self, n):
        return self.cards_.pop(n)

    def getbyid(self, id):
        for i, card in enumerate(self.cards_):
            if card.uuid_ == id:
                return i, card
        return None

    def takebyid(self, id):
        i, _ = self.getbyid(id)
        self.ncards_ -= 1
        return self.cards_.pop(i)

    def takeTop(self):
        self.ncards_ -= 1
        return self.cards_.pop()

    def __len__(self):
        return self.ncards_

    def __repr__(self):
        if self.ncards_ <= 20:
            return "{}".format(self.ncards_) + ' '+' '.join([str(el) for el in self.cards_])
        else:
            return "{}".format(self.ncards_)

    def __getitem__(self, item):
        return self.cards_[item]


class Hand(Pile):
    # Set of cards held by a player (see Game.py)
    def __init__(self):
        Pile.__init__(self)

    def __repr__(self):
        return '{:10}'.format('Hand:') + Pile.__repr__(self)


class Center(Pile):
    # Set of cards common to all players, min of 2 at each time
    def __init__(self):
        Pile.__init__(self)

    def new(self, deck, n):
        self.ncards_ = 0
        for _ in range(n):
            self.add(deck.takeTop())

    def __repr__(self):
        return '{:10}'.format("Center:")+Pile.__repr__(self)


class Discards(Pile):
    # Discard pile, no card should normally come out, except if the
    # deck is used up
    def __init__(self):
        Pile.__init__(self)

    def __repr__(self):
        return '{:10}'.format("Discards:")+Pile.__repr__(self)


class Deck(Pile):
    # deck of 108 defined cards
    def __init__(self):
        Pile.__init__(self)
        # for i in range(7):
        #     print(self.cards_[i])

    def new(self):
        # Create fresh deck of cards with given set of cards given by
        # the deck.csv file
        self.ncards_ = 0
        with open('resources/deck.csv', 'r') as fid:
            d = csv.reader(fid, delimiter=',')
            next(d)  # ignore header
            i = 0  # uuid for the card
            for col, num, rep in d:
                # create "rep" cards with number and color (num,col)
                for _ in range(int(rep)):
                    self.add(Card(Color[col], Number[num], i))
                    if col == 'JOKER':
                        self.cards_[-1].joker_ = 'color'
                    elif num == 'JOKER':
                        self.cards_[-1].joker_ = 'number'
                    i += 1

    def shuffle(self):
        shuffle(self.cards_)

    def __repr__(self):
        return '{:10}'.format("Deck:")+Pile.__repr__(self)
