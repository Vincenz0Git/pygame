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
            card = self.mp.checkCursorIn(Point2(*pygame.mouse.get_pos()))
            if event.type == pygame.QUIT:
                self.running_ = False
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos

                for c in self.mp.cards_:
                    c.isHovered_ = False
                if card:
                    card.isHovered_ = True

                if self.mp.draggedCard_:
                    card = self.mp.draggedCard_
                    try:
                        card.pos_ = (mouse_x + self.offx_, mouse_y + self.offy_)
                    except:
                        print('error')

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not card == self.mp.draggedCard_:
                    card.draggable_ = True
                    self.mp.draggedCard_ = False
                    self.mp.draggedCard_ = card

                mouse_x, mouse_y = event.pos
                self.offx_ = card.pos_[0] - mouse_x
                self.offy_ = card.pos_[1] - mouse_y

            if event.type == pygame.MOUSEBUTTONUP:
                if self.mp.draggedCard_:
                    self.mp.draggedCard_ = False


    def fill(self, color):
        self.screen_.fill(color)

    def flip(self):
        pygame.display.flip()


if __name__ == '__main__':
    #pygame.init()
    w = App()
