#!venv/bin/python

from Network.client import TCPClient

class GameClient(TCPClient):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    gc = GameClient()
    gc.send()
