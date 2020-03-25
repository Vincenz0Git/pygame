#!venv/bin/python
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


class TCPServer(socket.socket):
    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.clients_ = {}
        self.running_ = True
        self.host_ = "127.0.0.1"
        self.port_ = 9999
        self.messages_ = Queue()
        self.launch()

    def launch(self):
        self.bind((self.host_, self.port_))
        self.listen(5)
        self.newConnectionsThread = threading.Thread(target=self.newConnections)
        self.newConnectionsThread.start()
        self.newMessageThread = threading.Thread(target=self.newMessage)
        self.newMessageThread.start()
        while True:
            cmd = input()
            if cmd == 'quit':
                self.running_ = False
                self.close()
                self.messages_.put((-1, ""))
                self.newMessageThread.join()
                self.newConnectionsThread.join()
                for i, c in self.clients_.items():
                    c.state_ = State.LEFT
                    c.socket.close()
                    c.join()
                break



    def addClient(self, client, id):
        self.clients_[id] = client

    def getNewId(self):
        for i in range(len(self.clients_)):
            if not self.clients_.get(i) == i:
                return i
        return len(self.clients_)

    def anyDisconnect(self):
        pass
    # Wait for new connections
    def newConnections(self):

        while self.running_:
            try:
                sock, address = self.accept()
                id = self.getNewId()
                self.addClient(Client(sock, address, id, "Name", True, self.messages_), id)
                self.clients_[id].start()
                print("New connection at ID " + str(self.clients_[id]))
            except ConnectionAbortedError:
                print('Closing new connection thread')
                break


    def newMessage(self):
        while self.running_:
            id, msg = self.messages_.get()
            if id == -1:
                print("Closing new Messages thread")
                break
            if msg == b'end':
                self.clients_[id].state_ = State.LEFT
                self.clients_[id].join()
                self.removeClient(id)
            else:
                print(id, msg)

    def removeClient(self, id):
        self.clients_.pop(id)

    def kill(self):
        self.running_ = False


class Client(threading.Thread):
    # Client class, new instance created for each connected client
    # Each instance has the socket and address that is associated with items
    # Along with an assigned ID and a name chosen by the client
    def __init__(self, socket, address, id, name, signal, queue):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.queue_ = queue
        self.state_ = State.CONNECTED

    def __str__(self):
        return str(self.id) + " " + str(self.address)


    def reconnect(self):
        pass

    # Attempt to get data from client
    # If unable to, assume client has disconnected and remove him from server data
    # If able to and we get data back, print it in the server and send it back to every
    # client aside from the client that has sent it
    # .decode is used to convert the byte data into a printable string
    def run(self):
        while self.state_ == State.CONNECTED:
            try:
                data = self.socket.recv(32)
            except OSError:
                print('Server down, ending client', self.id)
                break
            if data != b'':
                self.queue_.put((self.id, data))
            elif self.state_ == State.LEFT:
                print("Disconnected ID "+str(self))
            else:
                self.state_ = State.DISCONNECTED
                print('lost connextion')



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
