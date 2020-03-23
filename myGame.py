from myCards import Deck, CenterCards


class Game:
    def __init__(self):
        self.players_ = []
        self.turn_ = 0
        self.deck_ = Deck()
        self.nPlayers_ = 0
        self.centralCards_ = CenterCards()

    def addPlayer(self, player):
        print('new player join')
        self.players_.append(player)

    def dealAll7(self):
        for player in self.players_:
            player.dealn(self.deck_, 7)
        print(self.deck_, self.centralCards_, self.players_[0])

    def new(self, nPlayers):
        for _ in range(nPlayers):
            self.addPlayer(Player())

        self.deck_.new()
        self.deck_.shuffle()
        self.turn_ = 0
        self.nPlayers_ = nPlayers
        self.centralCards_.new(self.deck_, 2)
        print(self.deck_, self.centralCards_, self.players_[0])




class Player:
    def __init__(self):
        self.hand_ = []

    def deal1(self, deck):
        self.hand_.append(deck.takeTopCard())

    def dealn(self, deck, n):
        for _ in range(n):
            self.deal1(deck)

    def play1(self,central):
        pass

    def __repr__(self):
        return ' '.join([str(el) for el in self.hand_])
