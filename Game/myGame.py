from Game.myCards import Deck, Center, Discards, Hand
from Game.cst import Number, Color, Bonus
from Game.myPlayers import Player
from Game.gameMechanics import Play, Engine
from threading import Thread

# probably a better way
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

    def askToDraw(self, player):
        player.deal1(self.deck_)

    def askToPutCard(self, player):
        a = self.askInput('Put a card: ')
        self.centralCards_.add(player.hand_.takebyid(int(a)))

    def checkNoPlays(self):
        for play in self.currentPlayer_.plays_:
            if not play.noPlay():
                return False
        return True

    def endTurn(self):
        self.currentPlayer_.getBonus()
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
        for bonus in self.currentPlayer_.bonus_:
            if bonus == Bonus.COLOR1:
                self.askToPutCard(self.currentPlayer_)
            elif bonus == Bonus.COLOR2:
                self.askToPutCard(self.currentPlayer_)
                for player in self.players_:
                    if not player == self.currentPlayer_:
                        self.askToDraw(player)

    def askJoker(self, card):
        while True:
            try:
                if card.joker_ == 'color' and card.color_ == Color.JOKER:
                    val = self.askInput(self.currentPlayer_, str(card) + ' ' + card.joker_ + ':')
                    card.color_ = Color[val]
                elif card.joker_ == 'number' and card.number_ == Number.JOKER:
                    val = self.askInput(self. currentPlayer_, str(card) + ' ' + card.joker_ + ':')
                    card.number_ = Number(int(val))
            except:
                    pass
            else:
                break

    def sendToPlayer(self, player, msg):
        # to be overwritten
        print(msg)

    def askInput(self, player, msg):
        # to be overwritten
        return input(msg)

    def takeBack(self):
        fromHand, inBoard = self.currentPlayer_.getLastPlay()
        if fromHand.joker_ == 'color':
            fromHand.color_ = Color.JOKER
        if fromHand.joker_ == 'number':
            fromHand.number_ = Number.JOKER
        if inBoard.joker_ == 'color':
            inBoard.color_ = Color.JOKER
        if inBoard.joker_ == 'number':
            inBoard.number_ = Number.JOKER
        self.currentPlayer_.hand_.add(fromHand)

    def getAllPlays(self):
        self.sendToPlayer(self.currentPlayer_, str(self.centralCards_) + "\n" + str(self.currentPlayer_))
        playInput = self.askInput(self.currentPlayer_, 'play: ')
        endTurn = False
        while not endTurn:
            if (playInput == 'draw' and not self.replay_):
                self.askToDraw(self.currentPlayer_)
                self.replay_ = True
            elif playInput == 'done':
                if self.replay_ and self.checkNoPlays():
                    self.askToPutCard(self.currentPlayer_)
                elif not self.checkNoPlays() and self.currentPlayer_.allPlaysRight():
                    self.sendToPlayer(self.currentPlayer_, 'ending turn')
                    endTurn = True
                    break
                else:
                    self.sendToPlayer(self.currentPlayer_, 'some plays are still wrong')
            elif playInput == 'takeback':
                try:
                    self.takeBack()
                except:
                    self.sendToPlayer(self.currentPlayer_, 'error taking back')
            else:
                try:
                    p = playInput.split(':')
                    fromHand = self.currentPlayer_.takeCardbyid(int(p[0]))
                    inBoard = self.centralCards_.getbyid(int(p[1]))[1]
                    if fromHand.joker_:
                        self.askJoker(fromHand)
                    if inBoard.joker_:
                        self.askJoker(inBoard)
                    self.currentPlayer_.addPlay(
                     fromHand,
                     inBoard
                    )
                except:
                    self.sendToPlayer(self.currentPlayer_, 'wrong play: valid are => [idHand]:[idCenter], draw, done')
                    pass
            self.sendToPlayer(self.currentPlayer_, '\n\n')
            self.sendToPlayer(self. currentPlayer_, str(self.centralCards_) + "\n" + str(self.currentPlayer_))
            playInput = self.askInput(self.currentPlayer_, 'play: ')

    def initTurn(self):
        self.currentPlayer_ = self.players_[self.turn_ % self.nPlayers_]
        self.replay_ = False
        for card in self.centralCards_:
            self.currentPlayer_.plays_.append(Play([], card))

    def takeTurn(self):
        self.initTurn()
        self.sendToPlayer(self.currentPlayer_, 'Turn: ' +str(self.turn_))
        self.getAllPlays()

        # When the plays are set and validated
        self.endTurn()
        self.sendToPlayer(self.currentPlayer_, 'End turn')
        self.sendToPlayer(self.currentPlayer_, '=======================================================')
        self.turn_ += 1
