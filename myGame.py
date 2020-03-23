from myCards import Deck, Center, Discards
from cst import Bonus


def itemgetter(*items):
    if len(items) == 1:
        item = items[0]

        def g(obj):
            return tuple([obj[item]])
    else:
        def g(obj):
            return tuple(obj[item] for item in items)
    return g


class Play:
    def __init__(self, inHand, inBoard):
        # inHand: list of Cards
        # inBoard Card
        self.inHand_ = inHand
        self.inBoard_ = inBoard

    def set(self, inHand, inBoard):
        self.inHand_ = inHand
        self.inBoard_ = inBoard

    def isRight(self):
        # Play is right if no card is played, one hand card is the same
        # as the one on the board, or two hand cards sum to the one on
        # the board
        if self.inBoard_ and len(self.inHand_) == 0:
            return True
        if len(self.inHand_) == 1:
            return self.inHand_[0].value() == self.inBoard_.value()
        elif len(self.inHand_) == 2:
            return self.inHand_[0].value() + self.inHand_[1].value() == self.inBoard_.value()
        else:
            return False

    def getBonus(self):
        color = self.inBoard_.color()
        if len(self.inHand_) == 1:
            if self.inHand_[0].color() == color:
                return Bonus.COLOR1
        elif len(self.inHand_) == 2:
            if self.inHand_[0].color() == self.inHand_[1].color() == color:
                return Bonus.COLOR2
        else:
            return Bonus.NONE

    def __repr__(self):
        return str(self.inHand_) + "->" + str(self.inBoard_)


class Engine:
    def __init__(self):
        self.deck_ = Deck()
        self.centralCards_ = Center()
        self.discardPile_ = Discards()

    def new(self):
        self.deck_.new()
        #self.deck_.shuffle()
        self.centralCards_.new(self.deck_, 3)

    def checkPlay(self, play):
        if play.isRight():
            return True
        else:
            return False

    def checkBonus(self, play):
        return play.getBonus()


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
            player.dealn(self.deck_, 12)
        #print(self.deck_, self.centralCards_, self.players_[0])

        self.takeTurn()

    def new(self, nPlayers):
        Engine.new(self)
        for _ in range(nPlayers):
            self.addPlayer(Player())

        self.turn_ = 0
        self.nPlayers_ = nPlayers
        print(self.deck_, self.centralCards_, self.players_[0])

    def takeTurn(self):
        print('Turn: ', self.turn_)
        print('Board state: ', self.centralCards_)

        currentPlayer = self.players_[self.turn_ % self.nPlayers_]

        print('Player hand: ', currentPlayer)

        for i, card in enumerate(self.centralCards_):
            # input simulate what the gui will provide
            currentPlayer.setPlay(str(i), None, [])
            while not self.checkPlay(currentPlayer.plays_[str(i)]):
                a = input('Play for {}: '.format(card)).split()
                if len(a) == 0:
                    h = []
                else:
                    h = [int(el) for el in a]

                currentPlayer.setPlay(str(i), card, h)
                print('Play: ', currentPlayer.plays_[str(i)])

            print(self.checkBonus(currentPlayer.plays_[str(i)]))

        print('End turn')
        print('=======================================================')

        self.turn_ += 1


class Player:
    def __init__(self):
        self.hand_ = []
        self.plays_ = {}

    def deal1(self, deck):
        self.hand_.append(deck.takeTopCard())

    def dealn(self, deck, n):
        for _ in range(n):
            self.deal1(deck)

    def setPlay(self, iplay, central, indicesHand):
        self.plays_[iplay] = Play(itemgetter(*indicesHand)(self.hand_), central)

    def __repr__(self):
        return '(Player '+' '.join([str(el) for el in self.hand_]) + ')'

    def __getitem__(self, item):
        return self.hand_[item]
