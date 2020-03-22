class Hand:
    def __init__(self):
        self.cards_ = []

    def add1(self, deck):
        self.cards_.append(deck.takeTopCard())

    def addn(self, deck, n):
        for _ in range(n):
            self.cards_.append(deck.takeTopCard())


class Player:
    def __init__(self):
        self.hand_ = Hand()

    def deal1(self, deck):
        self.hand_.add1(deck)

    def dealn(self, deck, n):
        self.hand_.addn(deck, n)
