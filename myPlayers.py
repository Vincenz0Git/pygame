class Hand:
    def __init__(self):
        self.cards_ = []

    def add1(self, deck):
        topdeck = deck.takeTopCard()
        self.cards_.append(topdeck)

    def addn(self, deck, n):
        for _ in range(n):
            self.add1(deck)


class Player:
    def __init__(self, hand):
        self.hand_ = hand

    def deal1(self, deck):
        self.hand_.add1(deck)

    def dealn(self, deck, n):
        self.hand_.addn(deck, n)
