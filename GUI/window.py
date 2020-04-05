#!venv/bin/python

import pygame
from pygame.locals import *
from GUI.mySprite import SpriteCards
from GUI.myDrawables import DrawableCard, MainPlayer
from GUI.myMath import Rec, Point2

import pygame.gfxdraw

from math import floor

RESOLUTION = (1000, 700)
MAINHANDSIZE = (700,150)
MAINHANDPOS = Point2(150,550)


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
        self.offx_ = 0
        self.offy_ = 0
        self.mp = MainPlayer(MAINHANDPOS, 0, MAINHANDSIZE, self.cardsSprites_)
        self.c1 = DrawableCard(self.cardsSprites_.getCardImage(1, 2, DrawableCard.CARDSIZE), (70,80), 30)
        self.mainLoop()

    def mainLoop(self):
        while self.running_:
            self.clock_.tick(60)
            self.handleEvents()

            self.screen_.blit(self.background_,(0,0))
            self.c1.draw(self.screen_,True)
            self.mp.draw(self.screen_)
            #pygame.draw.ellipse(self.screen_,(255,0,0),(0,0,500,200))
            #pygame.draw.rect(self.screen_, (0, 128, 255), pygame.Rect(30, 30, 60, 60))
            self.flip()

    def loadImage(self, file, zoom):
        image = pygame.image.load(file).convert()
        return pygame.transform.smoothscale(image,zoom)



    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running_ = False
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos

                for card in self.mp.cards_:
                    card.zoom_ = DrawableCard.CARDSIZE
                    card.isHovered_ = False

                card = self.mp.checkCursorIn(Point2(*event.pos))
                if card:
                    card.zoom_ = (180, 240)
                    card.isHovered_ = True
                    #print(card.pos_)

                if self.c1.isPointIn(Point2(mouse_x, mouse_y)):
                    self.c1.zoom_ = (140,200)
                else:
                    self.c1.zoom_ = DrawableCard.CARDSIZE

                if self.c1.draggable_:

                    try:
                        self.c1.pos_ = (mouse_x + self.offx_, mouse_y + self.offy_)
                    except:
                        print('error')

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.c1.isPointIn(Point2(*event.pos)):
                    print('select card')
                    mouse_x, mouse_y = event.pos
                    self.offx_ = self.c1.pos_[0] - mouse_x
                    self.offy_ = self.c1.pos_[1] - mouse_y
                    self.c1.draggable_ = True
                pass

            if event.type == pygame.MOUSEBUTTONUP:
                self.c1.draggable_ = False
                pass

    def fill(self, color):
        self.screen_.fill(color)

    def flip(self):
        pygame.display.flip()


if __name__ == '__main__':
    #pygame.init()
    w = App()
