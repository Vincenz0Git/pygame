from myCards import Deck, Center, Discards, Hand
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
        self.deck_.shuffle()
        self.centralCards_.new(self.deck_, 2)

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
            player.dealn(self.deck_, 7)
        #print(self.deck_, self.centralCards_, self.players_[0])

        self.takeTurn()
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
            # input simulate what the gui/network will provide
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

        # When the plays are set and validated
        for play in currentPlayer.plays_.values():
            for card in play.inHand_:
                # remove the cards from hand
                self.discardPile_.add(currentPlayer.takeCardbyid(card.uuid_))
            if len(play.inHand_) > 0:
                # remove the cards from the pile and replace them by new ones
                # from the deck
                print(play.inBoard_.uuid_)
                self.discardPile_.add(self.centralCards_.takebyid(play.inBoard_.uuid_))
                self.centralCards_.add(self.deck_.takeTop())

        print('End turn')

        print(currentPlayer, self.discardPile_)

        print('=======================================================')
        self.turn_ += 1


class Player:
    def __init__(self):
        self.hand_ = Hand()
        self.plays_ = {}

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

    def setPlay(self, iplay, central, indicesHand):
        self.plays_[iplay] = Play(itemgetter(*indicesHand)(self.hand_), central)

    def __repr__(self):
        return '(Player '+' '.join([str(el) for el in self.hand_]) + ')'

    def __getitem__(self, item):
        return self.hand_[item]
