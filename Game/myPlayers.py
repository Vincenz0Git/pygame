from Game.myCards import Hand

class Player:
    def __init__(self):
        self.hand_ = Hand()
        self.plays_ = {}
        self.bonus_ = []

    def deal1(self, deck):
        self.hand_.add(deck.takeTop())

    def dealn(self, deck, n):
        for _ in range(n):
            self.deal1(deck)

    def getCard(self, n):
        # get the nth card of the hand and remove it
        return self.hand_.pop(n)

    def takeCardbyid(self, id):
        return self.hand_.takebyid(id)

    def setPlay(self, iplay, play):
        self.plays_[iplay] = play

    def __repr__(self):
        return '(Player '+ str(self.hand_) + ')'

    def __getitem__(self, item):
        return self.hand_[item]
