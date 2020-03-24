from myCards import Deck, Center, Discards, Hand
from cst import Number, Color, Bonus
from myPlayers import Player
from gameMechanics import Play, Engine


def itemgetter(*items):
    if len(items) == 1:
        item = items[0]

        def g(obj):
            return tuple([obj[item]])
    else:
        def g(obj):
            return tuple(obj[item] for item in items)
    return g


class Game(Engine):
    def __init__(self):
        Engine.__init__(self)
        self.deck_ = Deck()
        self.centralCards_ = Center()
        self.discardPile_ = Discards()
        self.players_ = []
        self.turn_ = 0
        self.nPlayers_ = 0
        self.currentPlayer_ = None
        self.end_ = False

    def addPlayer(self, player):
        print('new player join')
        self.players_.append(player)

    def dealAlln(self, n):
        for player in self.players_:
            player.dealn(self.deck_, n)

    def launch(self):
        while not self.end_:
            self.takeTurn()

    def new(self, nPlayers):
        self.deck_.new()
        print('Fresh deck:', self.deck_.ncards_)
        #self.deck_.shuffle()
        self.centralCards_.new(self.deck_, 2)
        for _ in range(nPlayers):
            self.addPlayer(Player())

        self.end_ = False
        self.turn_ = 0
        self.nPlayers_ = nPlayers
        print(self.deck_, self.centralCards_, self.players_[0])

    def askJoker(self, card):
        if card.joker_ == 'number':
            self.askNumber(card)
        elif card.joker_ == 'color':
            self.askColor(card)

    def askColor(self, card):
        col = input(str(card) + " color? ")
        card.color_ = Color[col]

    def askNumber(self, card):
        num = input(str(card) + " number? ")
        card.number_ = Number[num]

    def askToDraw(self, player):
        player.deal1(self.deck_)

    def askToPutCard(self, player):
        a=input('Put a card: ')
        self.centralCards_.add(player.hand_.takebyid(player.hand_[int(a)].uuid_))


    def checkNoPlays(self):
        for play in self.currentPlayer_.plays_.values():
            if not play.noPlay():
                return False
        return True

    def endTurn(self):
        for play in self.currentPlayer_.plays_.values():
            for card in play.inHand_:
                # remove the cards from hand
                self.discardPile_.add(self.currentPlayer_.takeCardbyid(card.uuid_))
            if len(play.inHand_) > 0:
                # remove the cards from the pile and replace them by new ones
                # from the deck
                print(play.inBoard_.uuid_)
                self.discardPile_.add(self.centralCards_.takebyid(play.inBoard_.uuid_))
                self.centralCards_.add(self.deck_.takeTop())

    def getPlayForCard(self, card):
        # Simulation of network/GUI
        a = input('Play for {}: '.format(card)).split()
        if len(a) == 0:
            h = []
        else:
            h = [int(el) for el in a]

        toPlayFromHand = itemgetter(*h)(self.currentPlayer_.hand_)

        self.askJoker(card)
        for c in toPlayFromHand:
            self.askJoker(c)

        return Play(toPlayFromHand, card)

    def getAllPlays(self, replay=False):
        if replay:
            print('replay..')
        for i, card in enumerate(self.centralCards_):
            # input simulate what the gui/network will provide
            play = Play()
            while not self.checkPlay(play):

                play = self.getPlayForCard(card)

            self.currentPlayer_.setPlay(str(i), play)
            self.currentPlayer_.bonus_.append(self.checkBonus(play))

            print(self.checkBonus(play))

        if not replay and self.checkNoPlays():
            self.askToDraw(self.currentPlayer_)
            self.getAllPlays(replay=True)

        if replay and self.checkNoPlays():
            self.askToPutCard(self.currentPlayer_)

        if len(self.currentPlayer_.hand_) == 0:
            self.end_ = True
            print('Player WIN!!!!')

    def initTurn(self):
        self.currentPlayer_ = self.players_[self.turn_ % self.nPlayers_]

    def takeTurn(self):
        print('Turn: ', self.turn_)
        print('Board state: ', self.centralCards_)

        self.initTurn()

        print('Player hand: ', self.currentPlayer_)

        self.getAllPlays(replay=False)

        # When the plays are set and validated
        self.endTurn()

        print('End turn')

        print(self.currentPlayer_, self.discardPile_)

        print('=======================================================')
        self.turn_ += 1
