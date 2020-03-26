#!../venv/bin/python
import socket
import threading
from queue import Queue
import time
# Variables for holding information about connections

#TODO disconnecting: end request or recv()->b''

from enum import Enum


class State(Enum):
    CONNECTED    = 0
    LEFT         = 1
    DISCONNECTED = 2


class LOG(Enum):
    INFO = 0
    WARNING = 1
    ERROR = 2


class TCPServer(socket.socket):
    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.clients_ = {}
        self.running_ = True
        self.host_ = "127.0.0.1"
        self.port_ = 9999
        self.messages_ = Queue()

    def log(self, type, msg):
        print(type.name + ': ' + msg)


    def startServer(self):
        self.bind((self.host_, self.port_))
        self.listen(5)
        self.newConnectionsThread = threading.Thread(target=self.newConnections)
        self.newConnectionsThread.start()
        self.newMessageThread = threading.Thread(target=self.newMessage)
        self.newMessageThread.start()
        self.log(LOG.INFO, 'Server started')


    def mainLoop(self):
        # Blocking process, wait for user input
        while True:
            cmd = input()
            if cmd == 'quit':
                self.kill()
                break

    def addClient(self, client, uid):
        self.clients_[uid] = client

    def getNewuid(self):
        for i in range(len(self.clients_)):
            if not self.clients_.get(i) == i:
                return i
        return len(self.clients_)

    def disconnectedClients(self):
        for uid, client in self.clients_.items():
            if client.state_ == State.DISCONNECTED:
                yield uid, client
    # Wait for new connections
    def newConnections(self):

        while self.running_:
            try:
                sock, address = self.accept()
                for uid, client in self.disconnectedClients():
                    if address[0] == client.address[0]:
                        self.clients_[uid].socket = sock
                        self.clients_[uid].state_ = State.CONNECTED
                        print('client reconnected')
                        break
                else:
                    uid = self.getNewuid()
                    self.addClient(Client(sock, address, uid, "Name", True, self.messages_), uid)
                    self.clients_[uid].start()
                    self.log(LOG.INFO, "New connection at uid " + str(self.clients_[uid]))
            except ConnectionAbortedError:
                self.log(LOG.INFO, 'Closing new connection thread')
                break

    def newMessage(self):
        while self.running_:
            uid, msg = self.messages_.get()
            self.handleNewMessage(msg, uid)

    def handleNewMessage(self, msg, uid):
        if uid == -1:
            self.running_ = False
            self.log(LOG.INFO, "Closing new Messages thread")
        else:
            if msg == b'quit':
                self.clients_[uid].state_ = State.LEFT
                self.clients_[uid].join()
                self.removeClient(uid)
            else:
                self.log(LOG.INFO, str(uid)+' '+str(msg))
                self.sendToAll(msg)

    def sendToUid(self, msg, uid):
        self.clients_[uid].sendMessage(msg)

    def sendToAll(self, msg):
        for cl in self.clients_.values():
            cl.sendMessage(msg)

    def removeClient(self, uid):
        self.clients_.pop(uid)

    def kill(self):
        self.running_ = False
        self.close()
        self.messages_.put((-1, b"quit"))
        self.newMessageThread.join()
        self.newConnectionsThread.join()
        for i, c in self.clients_.items():
            c.state_ = State.LEFT
            c.socket.close()
            c.join()


class Client(threading.Thread):
    # Client class, new instance created for each connected client
    # Each instance has the socket and address that is associated with items
    # Along with an assigned uid and a name chosen by the client
    def __init__(self, socket, address, uid, name, signal, queue):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.uid = uid
        self.name = name
        self.queue_ = queue
        self.state_ = State.CONNECTED

    def __str__(self):
        return str(self.uid) + " " + str(self.address)

    def log(self, type, msg):
        print(type.name + ': ' + msg)

    def reconnect(self):
        pass

    def sendMessage(self, msg):
        self.socket.sendall(msg)

    # Attempt to get data from client
    # If unable to, assume client has disconnected and remove him from server data
    # If able to and we get data back, print it in the server and send it back to every
    # client asuide from the client that has sent it
    # .decode is used to convert the byte data into a printable string
    def run(self):
        while not self.state_ == State.LEFT:
            try:
                data = self.socket.recv(32)
            except OSError:
                self.log(LOG.INFO, 'Server down, ending client' + str(self.uid))
                break
            if data != b'':
                self.queue_.put((self.uid, data))
            elif self.state_ == State.LEFT:
                self.log(LOG.INFO, "Disconnected uid "+str(self))
            else:
                self.state_ = State.DISCONNECTED
                self.log(LOG.INFO, 'Lost connection with '+str(self.uid)+'timeout in ..')
                time.sleep(2)



def test():
    import socket
    import time
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 9999))
    s.listen(5)
    s2, a = s.accept()
    while True:
        try:
            msg = s2.recv(32)
            if msg == b'':
                print("connexion lost: wait for reconnect")
                time.sleep(1)
            else:
                print(msg)

        except KeyboardInterrupt:
            s2.close()
            break

if __name__ == '__main__':
    s = TCPServer()
    s.startServer()
    s.mainLoop()
