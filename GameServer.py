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

    def handleNewMessage(self, msg, uid):
        if uid == -1:
            # Server commands
            self.running_ = False
            self.log(LOG.INFO, "Closing new Messages thread")
        else:
            # Client commands
            if msg == b'quit':
                self.clients_[uid].state_ = State.LEFT
                self.clients_[uid].join()
                self.removeClient(uid)
            elif msg == b'/roomstate':
                self.clients_[uid].sendMessage(self.getRoomState().encode())
            elif b'/join' in msg:
                _, room = msg.decode().split()
                currentRoom = self.getRoomOfuid(uid)
                if currentRoom == room:
                    self.clients_[uid].sendMessage(('already joined room '+str(room)).encode())
                elif currentRoom:
                    self.rooms_[currentRoom].remove(uid)

                if uid not in self.rooms_[int(room)]:
                    self.rooms_[int(room)].add(uid)
                    self.clients_[uid].sendMessage(('joined room '+str(room)).encode())
            elif b'/leave' in msg:
                currentRoom = self.getRoomOfuid(uid)
                self.rooms_[currentRoom].remove(uid)
                self.clients_[uid].sendMessage(('leaved room '+str(currentRoom)).encode())

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
