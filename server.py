#!venv/bin/python
import socket
import threading
# Variables for holding information about connections


class Server(socket.socket):
    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.clients_ = {}
        self.running_ = True
        self.host_ = "127.0.0.1"
        self.port_ = 9999
        self.launch()

    def launch(self):
        self.bind((self.host_, self.port_))
        self.listen(5)
        self.newConnectionsThread = threading.Thread(target=self.newConnections)
        self.newConnectionsThread.start()

    def addClient(self, client, id):
        self.clients_[id] = client

    # Wait for new connections
    def newConnections(self):
        id = 0
        while self.running_:
            sock, address = self.accept()
            self.addClient(Client(sock, address, id, "Name", True), id)
            self.clients_[id].start()
            print("New connection at ID " + str(self.clients_[id]))

    def kill(self):
        self.running_ = False

# Client class, new instance created for each connected client
# Each instance has the socket and address that is associated with items
# Along with an assigned ID and a name chosen by the client
class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal

    def __str__(self):
        return str(self.id) + " " + str(self.address)

    # Attempt to get data from client
    # If unable to, assume client has disconnected and remove him from server data
    # If able to and we get data back, print it in the server and send it back to every
    # client aside from the client that has sent it
    # .decode is used to convert the byte data into a printable string
    def run(self):
        while self.signal:
            try:
                data = self.socket.recv(32)
            except:
                print("Client " + str(self.address) + " has disconnected")
                self.signal = False
                #connections.remove(self)
                break
            if data != "":
                print("ID " + str(self.id) + ": " + str(data.decode("utf-8")))
                if str(data.decode("utf-8")) == "end":
                    self.signal = False
                for client in connections:
                    if client.id != self.id:
                        client.socket.sendall(data)



def main():
    # Get host and port

    s = Server()
    input('Press to end...')
    s.kill()
    #Create new thread to wait for connections


main()
