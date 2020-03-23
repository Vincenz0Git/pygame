from myCards import Deck, Center, Discards


class Engine:
    def __init__(self):
        self.deck_ = Deck()
        self.centralCards_ = Center()
        self.discardPile_ = Discards()

    def new(self):
        self.deck_.new()
        #self.deck_.shuffle()
        self.centralCards_.new(self.deck_, 2)

    def checkPlay(self,cardsToPlay,toCenterCard):
        if len(cardsToPlay) == 1:
            return cardsToPlay[0] == 1


class Game(Engine):
    def __init__(self):
        Engine.__init__(self)
        self.players_ = []
        self.turn_ = 0
        self.nPlayers_ = 0

    def addPlayer(self, player):
        print('new player join')
        self.players_.append(player)

    def dealAll7(self):
        for player in self.players_:
            player.dealn(self.deck_, 7)
        print(self.deck_, self.centralCards_, self.players_[0])

    def new(self, nPlayers):
        Engine.new(self)
        for _ in range(nPlayers):
            self.addPlayer(Player())

        self.turn_ = 0
        self.nPlayers_ = nPlayers
        print(self.deck_, self.centralCards_, self.players_[0])




class Player:
    def __init__(self):
        self.hand_ = []

    def deal1(self, deck):
        self.hand_.append(deck.takeTopCard())

    def dealn(self, deck, n):
        for _ in range(n):
            self.deal1(deck)

    def play(self, central):
        pass

    def __repr__(self):
        return ' '.join([str(el) for el in self.hand_])
