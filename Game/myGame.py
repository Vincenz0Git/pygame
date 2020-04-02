from Game.myCards import Deck, Center, Discards, Hand
from Game.cst import Number, Color, Bonus
from Game.myPlayers import Player
from Game.gameMechanics import Play, Engine
from threading import Thread


def itemgetter(*items):
    if len(items) == 1:
        item = items[0]

        def g(obj):
            return tuple([obj[item]])
    else:
        def g(obj):
            return tuple(obj[item] for item in items)
    return g


class Game(Engine, Thread):
    def __init__(self, uid):
        Engine.__init__(self)
        Thread.__init__(self)
        self.deck_ = Deck()
        self.centralCards_ = Center()
        self.discardPile_ = Discards()
        self.players_ = []
        self.turn_ = 0
        self.nPlayers_ = 0
        self.currentPlayer_ = None
        self.end_ = False
        self.uid_ = uid
        self.replay_ = False


    def addPlayer(self, player):
        print('new player join')
        self.players_.append(player)

    def dealAlln(self, n):
        for player in self.players_:
            player.dealn(self.deck_, n)

    def run(self):
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
        a=getInput('Put a card: ')
        self.centralCards_.add(player.hand_.takebyid(player.hand_[int(a)].uuid_))


    def checkNoPlays(self):
        for play in self.currentPlayer_.plays_:
            if not play.noPlay():
                return False
        return True

    def endTurn(self):
        for play in self.currentPlayer_.plays_:
            for card in play:
                # remove the cards from hand
                self.discardPile_.add(card)
                if len(play) > 0:
                    # remove the cards from the pile and replace them by new ones
                    # from the deck
                    self.discardPile_.add(self.centralCards_.takebyid(play.inBoard_.uuid_))
                    self.centralCards_.add(self.deck_.takeTop())
        self.currentPlayer_.plays_ = []

    def getInput(self):
        # to be overwritten, must return a str object

        return input('Play: ')

    def sendOutput(self, msg):
        # to be overwritten
        print(msg)

    def askInput(self, msg):
        # to be overwritten
        return input(msg)

    def getAllPlays(self):
        self.sendOutput(str(self.centralCards_) + "\n" + str(self.currentPlayer_))
        playInput = self.getInput()
        endTurn = False
        while not endTurn:
            if (playInput == 'draw' and not self.replay_):
                self.askToDraw(self.currentPlayer_)
                self.replay_ = True
            elif playInput == 'done' and (not self.checkNoPlays() or self.replay_):
                print('ending turn')
                endTurn = True
                break
            elif playInput == 'takeback':
                try:
                    fromHand, inBoard = self.currentPlayer_.getLastPlay()
                    self.currentPlayer_.hand_.add(fromHand)
                except:
                    print('error taking back')
            else:
                try:
                    p = playInput.split(':')
                    self.currentPlayer_.addPlay(
                     self.currentPlayer_.takeCardbyid(int(p[0])),
                     self.centralCards_.getbyid(int(p[1]))[1]
                    )
                except:
                    print('wrong play')
                    pass
            self.sendOutput(str(self.centralCards_) + "\n" + str(self.currentPlayer_))
            playInput = self.getInput()

        self.endTurn()

    def getPlayForCard(self, card):
        # Simulation of network/GUI
        a = input('Play for {}: '.format(card)).split()
        if 'quit' in a:
            self.end_ = True
            return None
        if len(a) == 0:
            h = []
        else:
            h = [int(el) for el in a]

        toPlayFromHand = itemgetter(*h)(self.currentPlayer_.hand_)

        self.askJoker(card)
        for c in toPlayFromHand:
            self.askJoker(c)

        return Play(toPlayFromHand, card)

    def getaaAllPlays(self, replay=False):
        if replay:
            print('replay..')
        for i, card in enumerate(self.centralCards_):
            # input simulate what the gui/network will provide
            play = Play()
            try:
                while not self.checkPlay(play):
                    play = self.getPlayForCard(card)
            except AttributeError:
                break

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
        self.replay_ = False

    def takeTurn(self):
        print('Turn: ', self.turn_)
        #print(self.centralCards_)

        self.initTurn()

        #print(self.currentPlayer_)

        self.getAllPlays()

        # When the plays are set and validated
        self.endTurn()

        print('End turn')

        #print(self.currentPlayer_, self.discardPile_)

        print('=======================================================')
        self.turn_ += 1
