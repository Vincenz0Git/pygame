#!../venv/bin/python
import socket
import threading
from queue import Queue
import time

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
    """
    Create a TCP server on address/port given in the resources/ip.txt file.
    defines a thread to handle the new connections from clients and another
    to handle the messages coming from the clients.

    The main loop is for the moment done in the main thread.

    The clients_ are organized in {uid:Client()}

    handleNewMessage is meant to be overriden in the child classes.

    messages_ is a queue that gets the messages from all the clients and then
    is processed in the newMessageThread. All the clients share the same queue

    >>  s = TCPServer()
    >>  s.startServer()
    >>  s.mainLoop()
    """

    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.clients_ = {}
        self.running_ = True
        with open("resources/ip.txt","r") as fid:
            self.host_ = fid.read().strip()
        self.port_ = 9999
        self.messages_ = Queue()

    def log(self, type, msg):
        print(type.name + ': ' + msg)

    def startServer(self):
        print('Host: ',self.host_,' change in resources/ip.txt')
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
            self.messages_.put((-1, cmd.encode()))
            if '/quit' in cmd:
                self.kill()
                break

    def addClient(self, client, uid):
        self.clients_[uid] = client

    def getClientuid(self, client):
        for uid, cl in self.clients_.items():
            if client.uid_ == uid:
                return uid
        return None

    def getClientbyuid(self, uid):
        for client in self.clients_.values():
            if client.uid_ == uid:
                return client
        return None

    def getNewuid(self):
        ids = self.clients_.keys()
        for i in range(len(self.clients_)):
            if not i in ids:
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
                break

        self.log(LOG.INFO, 'Closing new connection thread a')

    def newMessage(self):
        # Target for the newMessageThread
        while self.running_:
            uid, msg = self.messages_.get()
            self.handleNewMessage(msg, uid)
            self.messages_.task_done()

        self.log(LOG.INFO, "Closing new Messages thread")

    def handleNewMessage(self, msg, uid):
        if uid == -1:
            self.running_ = False
        else:
            if msg == b'quit':
                self.clients_[uid].state_ = State.LEFT
                self.clients_[uid].join()
                self.removeClient(self.clients_[uid])
            else:
                self.log(LOG.INFO, str(uid)+' '+str(msg))
                self.sendToAll(msg)

    def sendToUid(self, msg, uid):
        self.clients_[uid].sendMessage(msg)

    def sendToAll(self, msg):
        for cl in self.clients_.values():
            cl.sendMessage(msg)

    def removeClient(self, client):
        self.clients_.pop(client.uid_)

    def kill(self):
        self.messages_.join()
        self.close()
        self.newMessageThread.join()
        self.newConnectionsThread.join()
        for i, c in self.clients_.items():
            c.state_ = State.LEFT
            c.socket_.close()
            c.join()


class Client(threading.Thread):
    """
    Client class, new instance created for each connected client
    Each instance has the socket and address that is associated with items
    Along with an assigned uid

    queue_ is the queue shared with the TCPServer, new messages received are
    put in it with the uid of the client.
    """

    def __init__(self, socket, address, uid, name, signal, queue):
        threading.Thread.__init__(self)
        self.socket_ = socket
        self.address_ = address
        self.uid_ = uid
        self.name_ = uid
        self.queue_ = queue
        self.state_ = State.CONNECTED
        self.ready_ = False
        self.inGame_ = False

    def __str__(self):
        return str(self.uid_) + " " + str(self.address_)

    def log(self, type, msg):
        print(type.name + ': ' + msg)

    def reconnect(self):
        pass

    def sendMessage(self, msg):
        self.socket_.sendall(msg)

    def run(self):
        while not self.state_ == State.LEFT:
            try:
                data = self.socket_.recv(32)
            except OSError:
                self.log(LOG.INFO, 'Server down, ending client' + str(self.uid_))
                break
            if data != b'':
                self.queue_.put((self.uid_, data))
            elif self.state_ == State.LEFT:
                self.log(LOG.INFO, "Disconnected uid "+str(self))
            else:
                self.state_ = State.DISCONNECTED
                self.log(LOG.INFO, 'Lost connection with '+str(self.uid_)+'timeout in ..')
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
