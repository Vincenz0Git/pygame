#!venv/bin/python

from Network.server import TCPServer, State, LOG
from Game.myGame import Game


class GameServer(TCPServer, Game):
    def __init__(self):
        TCPServer.__init__(self)
        Game.__init__(self)
        self.rooms_ = {1:set(), 2:set()}

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
        if uid == -1:
            # Server commands
            self.running_ = False
            self.log(LOG.INFO, "Closing new Messages thread")
        else:
            sender = self.clients_[uid]
            # Client commands
            if b'/quit' in msg:
                sender.state_ = State.LEFT
                sender.join()
                self.removeClient(uid)
            elif b'/roomstate' in msg:
                sender.sendMessage(self.getRoomState().encode())
            elif b'/join' in msg:
                cmd = msg.decode().split()
                if not len(cmd) == 2 or not cmd[1].isdigit():
                    sender.sendMessage('/join [room number]'.encode())
                else:
                    room = cmd[1]
                    currentRoom = self.getRoomOfuid(uid)
                    if currentRoom == int(room):
                        sender.sendMessage(('Already joined room '+room).encode())
                    elif currentRoom:
                        self.rooms_[currentRoom].remove(uid)
                    try:
                        if uid not in self.rooms_[int(room)]:
                            self.rooms_[int(room)].add(uid)
                            sender.sendMessage(('Joined room '+str(room)).encode())
                    except KeyError:
                        sender.sendMessage('/join [room number]'.encode())

            elif b'/leave' in msg:
                currentRoom = self.getRoomOfuid(uid)
                self.rooms_[currentRoom].remove(uid)
                sender.ready_ = False
                sender.sendMessage(('leaved room '+str(currentRoom)).encode())

            elif b'/ready' in msg:
                if self.isInRoom(uid):
                    sender.ready_ = not sender.ready_
                    rep = 'You are' + ('' if sender.ready_ else ' not') + ' ready!'
                    sender.sendMessage(rep.encode())
                else:
                    sender.sendMessage('You are not in a room')

            else:
                self.log(LOG.INFO, str(uid)+' '+str(msg))
                #self.sendToAll(msg)
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
