#!../venv/bin/python

import socket
import threading
import sys


class TCPClient(socket.socket):
    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.host_ = "127.0.0.1"
        self.port_ = 9999
        self.signal_ = False
        self.receiveThread_ = threading.Thread(target=self.receive)
        self.settimeout(5.0)
        self.launch()

    def launch(self):
        try:
            self.connect((self.host_, self.port_))
            self.signal_ = True
            self.receiveThread_.start()
        except ConnectionRefusedError:
            print("Could not make a connection to the server")
            input("Press enter to quit")
            sys.exit(0)

    def receive(self):
        while self.signal_:
            try:
                data = self.recv(32)
                if data == b'':
                    print('lost connection to server')
                    break
                print(data.decode())
            except socket.timeout:
                continue

    def send(self):
        while self.signal_:
            message = input()
            self.sendall(str.encode(message))
            if message == "quit":
                self.signal_ = False
                #self.close()
                self.receiveThread_.join()
                #self.close()
        print('ending...')
        super().close()


def test():
    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 9999))

    while True:
        try:
            s.sendall(input().encode())
        except KeyboardInterrupt:
            s.close()
            break

if __name__ == '__main__':
    a = TCPClient()
    a.send()





#Send data to server
#str.encode is used to turn the string message into bytes so it can be sent across the network
