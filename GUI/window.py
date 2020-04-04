#!venv/bin/python

import pygame
from pygame.locals import *
from GUI.mySprite import SpriteCards

from math import floor

RESOLUTION = (1000, 700)
CARDSIZE = (120,200)

def scaleTuple(t,scale):
    return floor(t[0]*scale), floor(t[1]*scale)


class App:
    def __init__(self):
        pygame.init()
        self.screen_ = pygame.display.set_mode(RESOLUTION)
        self.clock_ = pygame.time.Clock()
        self.running_ = True
        self.background_ = self.loadImage("resources/table2.png", scaleTuple(RESOLUTION, 1))
        self.cardsSprites_ = SpriteCards('resources/sprites.png')
        self.c1 = self.cardsSprites_.getCardImage(1, 2, CARDSIZE)
        self.mainLoop()

    def mainLoop(self):
        while self.running_:
            self.clock_.tick(60)
            self.handleEvents()

            self.screen_.blit(self.background_,(0,0))
            self.screen_.blit(self.c1,(100,100))
            #pygame.draw.ellipse(self.screen_,(255,0,0),(0,0,500,200))
            pygame.draw.rect(self.screen_, (0, 128, 255), pygame.Rect(30, 30, 60, 60))
            self.flip()

    def loadImage(self, file, zoom):
        image = pygame.image.load(file).convert()
        return pygame.transform.smoothscale(image,zoom)



    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running_ = False

    def fill(self, color):
        self.screen_.fill(color)

    def flip(self):
        pygame.display.flip()


if __name__ == '__main__':
    #pygame.init()
    w = App()
