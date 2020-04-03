#!venv/bin/python

import os
import sys
sys.path.append(os.getcwd())

from Game.myGame import Game


g = Game(1)
g.new(1)
g.dealAlln(7)
g.start()
