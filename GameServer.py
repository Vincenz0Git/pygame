#!venv/bin/python

from Network.server import TCPServer, State, LOG
from Game.myGame import Game


class CommandException(BaseException):
    def __init__(self, msg):
        super().__init__()
        self.msg_ = msg


class GameServer(TCPServer, Game):
    def __init__(self):
        TCPServer.__init__(self)
        Game.__init__(self)
        self.rooms_ = {1:set(), 2:set()}
        self.commandsClient_ = {}
        self.initCmdsClient()

    def initCmdsClient(self):

        def quit(sender, *args):
            sender.state_ = State.LEFT
            sender.join()
            self.removeClient(sender)

        def roomstate(sender, *args):
            sender.sendMessage(self.getRoomState().encode())

        def join(sender, *args):
            roomid = args[0][0]
            currentRoom = self.getRoomOfuid(sender.uid)
            if not len(args[0]) == 1 or not roomid.isdigit() or int(roomid) not in self.rooms_.keys():
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
                if sender.ready_:
                    self.messages_.put((-1, b"/checkready"))
            else:
                sender.sendMessage('You are not in a room'.encode())

        self.commandsClient_['/quit'] = quit
        self.commandsClient_['/roomstate'] = roomstate
        self.commandsClient_['/join'] = join
        self.commandsClient_['/leave'] = leave
        self.commandsClient_['/ready'] = ready

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
            if '/quit' in cmd[0]:
                self.running_ = False
                self.log(LOG.INFO, "Closing new Messages thread")

            if '/checkready' in cmd[0]:
                allReady = True
                for cl in self.clients_.values():
                    if not cl.ready_:
                        allReady = False
                if allReady:
                    self.sendToAll('Everyone ready!'.encode())
        else:
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
