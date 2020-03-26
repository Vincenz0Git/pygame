#!venv/bin/python

from Network.server import TCPServer, State, LOG
from Game.myGame import Game


class GameServer(TCPServer, Game):
    def __init__(self):
        TCPServer.__init__(self)
        Game.__init__(self)

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
            else:
                self.log(LOG.INFO, str(uid)+' '+str(msg))
                self.sendToAll(msg)


if __name__ == '__main__':
    gs = GameServer()
    gs.startServer()
    #gs.new(1)
    #gs.dealAlln(7)
    #gs.launch()
    gs.mainLoop()
