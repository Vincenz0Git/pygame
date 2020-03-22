class Game:
    def __init__(self):
        self.players_ = []

    def addPlayer(self, player):
        self.players_.append(player)

    def dealAll7(self, deck):
        for player in self.players_:
            player.dealn(deck, 7)
    def draw(self):
        pass
