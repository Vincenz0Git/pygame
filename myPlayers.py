class Hand:
    def __init__(self,):
        self.cards_ = []
    def deal7(self):
        pass

class Player:
    def __init__(self):
        self.hand_ = None

    def dealHand(self,deck):
        self.hand_ = Hand()
