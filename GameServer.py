#!venv/bin/python

from Network.server import TCPServer, State, LOG
from Game.myGame import Game
from Game.myPlayers import Player

from queue import Queue


helpMessage = """
-------------------------------------------------------------------------
Commands:
-------------------------------------------------------------------------
/join [roomid] -> Join a room
/ready         -> When in a room, toggle ready state
/leave         -> Leave the current room
/help          -> Print this menu
/play [play]   -> In game, submit a play, see valid plays
/roomstate     -> Print current room states
/quit          -> Leave the game
-------------------------------------------------------------------------
Cards display:
-------------------------------------------------------------------------
[Color][Number](id)  -> Joker as J
R1(112)
J1(89)
GJ(90)
...
-------------------------------------------------------------------------
Plays display:
-------------------------------------------------------------------------

[card1, card2] -> card3 (left is from the hand, right is on board)

valid plays:
113:112  -> put card 113 from the hand to card 112 on the board (use ids)
112      -> if card to put from the hand to the board asked (use ids)
1        -> if number of joker asked
RED      -> if color of joker asked
takeback -> takeback the last play
draw     -> draw one card
done     -> finish turn
-------------------------------------------------------------------------
"""


class PlayerOnline(Player):
    def __init__(self, socket):
        super().__init__()
        self.socket_ = socket

    def sendMessage(self, msg):
        self.socket_.sendall(msg.encode())



class CommandException(BaseException):
    def __init__(self, msg):
        super().__init__()
        self.msg_ = msg


class GameOnline(Game):
    def __init__(self, uid, queue):
        super().__init__(uid)
        self.clientSockets_ = {}
        self.queue_ = queue

    def new(self):
        self.deck_.new()
        self.sendToAll('Fresh deck: '+str(self.deck_.ncards_))
        #self.deck_.shuffle()
        self.centralCards_.new(self.deck_, 2)
        self.end_ = False
        self.turn_ = 0
        self.sendToAll(str(self.deck_)+str(self.centralCards_))

    def addPlayer(self, socket):
        self.nPlayers_ += 1
        self.players_.append(PlayerOnline(socket))

    def sendToPlayer(self, player, msg):
        # to be overwritten
        player.sendMessage(msg)

    def sendToAll(self, msg):
        for player in self.players_:
            player.sendMessage(msg)

    def askInput(self, player, msg):
        # to be overwritten
        player.sendMessage(msg)
        a = self.queue_.get()
        return a


class GameServer(TCPServer):
    def __init__(self):
        super().__init__()

        self.rooms_ = {1:set(), 2:set()}  # id:set of uid of players
        self.commandsClient_ = {}
        self.commandsServer_ = {}
        self.initCmdsClient()
        self.initCmdsServer()
        self.games_ = {}
        self.queues_ = {}

    def initCmdsServer(self):
        # List of server console commands
        def quit(*args):
            # Dont really know what happens here loul, but it works
            self.running_ = False
            self.log(LOG.INFO, "Quitting...")

        def cheackready(*args):
            state = {}
            for i, room in self.rooms_.items():
                if len(room) == 0:
                    state[i] = False
                    continue
                for uid in room:
                    if not self.clients_[uid].ready_:
                        state[i] = False
                        break
                else:
                    state[i] = True
                    startmsg = "/startgame "+str(i)
                    self.messages_.put((-1,startmsg.encode()))

            print(state)

        def startgame(*args):
            room = int(args[0][0])
            self.queues_[room] = Queue()
            self.games_[room] = GameOnline(room, self.queues_[room])
            self.games_[room].new()
            for uid in self.rooms_[room]:
                self.games_[room].addPlayer(self.clients_[uid].socket_)
            self.games_[room].dealAlln(7)
            self.games_[room].start()

        self.commandsServer_['/quit'] = quit
        self.commandsServer_['/checkready'] = cheackready
        self.commandsServer_['/startgame'] = startgame




    def initCmdsClient(self):
        # List of client console commands
        def quit(sender, *args):
            sender.state_ = State.LEFT
            sender.join()
            self.removeClient(sender)

        def roomstate(sender, *args):
            sender.sendMessage(self.getRoomState().encode())

        def join(sender, *args):
            roomid = args[0][0]
            currentRoom = self.getRoomOfuid(sender.uid)
            if not len(args[0]) == 1 or \
               not roomid.isdigit() or \
               int(roomid) not in self.rooms_.keys():
                raise CommandException('/join [room id]')
            elif not currentRoom == int(roomid):
                if currentRoom:
                    self.rooms_[currentRoom].remove(sender.uid)
                self.rooms_[int(roomid)].add(sender.uid)
                sender.sendMessage(('Joined room '+roomid).encode())
            else:
                # already in room, nothing to do
                pass

        def leave(sender, *args):
            currentRoom = self.getRoomOfuid(sender.uid)
            if currentRoom:
                self.rooms_[currentRoom].remove(sender.uid)
            sender.ready_ = False
            sender.sendMessage(('Leaved room '+str(currentRoom)).encode())

        def ready(sender, *args):
            if self.isInRoom(sender.uid):
                sender.ready_ = not sender.ready_
                rep = 'You are' + ('' if sender.ready_ else ' not') + ' ready!'
                sender.sendMessage(rep.encode())
                self.messages_.put((-1, b"/checkready"))
            else:
                sender.sendMessage('You are not in a room'.encode())

        def play(sender, *args):
            room = self.getRoomOfuid(sender.uid)
            print(args)
            self.queues_[room].put(args[0][0])

        def help(sender, *args):
            sender.sendMessage(helpMessage.encode())

        self.commandsClient_['/quit'] = quit
        self.commandsClient_['/roomstate'] = roomstate
        self.commandsClient_['/join'] = join
        self.commandsClient_['/leave'] = leave
        self.commandsClient_['/ready'] = ready
        self.commandsClient_['/play'] = play
        self.commandsClient_['/help'] = help


    def getRoomState(self):
        return ''.join(['Room '+str(n)+' -> '+str(len(players))+' players\n'
                        for n, players in self.rooms_.items()])

    def getRoomOfuid(self, uid):
        for r, players in self.rooms_.items():
            if uid in players:
                return r
        return None

    def isInRoom(self, uid):
        return not self.getRoomOfuid(uid) == None

    def handleNewMessage(self, msg, uid):

        cmd = msg.decode().split()
        if uid == -1:
            # Server commands
            # TODO dict commands list
            try:
                self.commandsServer_[cmd[0]](cmd[1:])
            except IndentationError:
                self.log(LOG.ERROR, 'Unknown server command')
        else:
            # Client commands
            sender = self.clients_[uid]
            try:
                self.commandsClient_[cmd[0]](sender, cmd[1:])
            except KeyError:
                sender.sendMessage('Unknown command'.encode())
            except CommandException as e:
                sender.sendMessage(e.msg_.encode())

    def initTurn(self):
        pass

    def getAllPlays(self, replay=False):
        pass


if __name__ == '__main__':
    gs = GameServer()
    gs.startServer()
    #gs.new(1)
    #gs.dealAlln(7)
    #gs.launch()
    gs.mainLoop()
