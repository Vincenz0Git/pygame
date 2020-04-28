#!venv/bin/python

import pygame
from pygame.locals import *
from GUI.mySprite import SpriteCards
from GUI.drawableEnv import Board
from GUI.myMath import Rec, Point2

import pygame.gfxdraw

from math import floor

from GUI.myCoord import *


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
        self.off_ = 0
        self.board_ = Board(self.cardsSprites_)
        #self.mp = MainPlayerZone(self.cardsSprites_)
        #self.c1 = DrawableCard(self.cardsSprites_.getCardImage(1, 2, DrawableCard.CARDSIZE), (70,80), 30)
        self.mainLoop()

    def mainLoop(self):
        while self.running_:
            self.clock_.tick(60)
            self.handleEvents()

            self.screen_.blit(self.background_,(0,0))
            self.board_.draw(self.screen_)
            #pygame.draw.ellipse(self.screen_,(255,0,0),(0,0,500,200))
            #pygame.draw.rect(self.screen_, (0, 128, 255), pygame.Rect(30, 30, 60, 60))
            self.flip()

    def loadImage(self, file, zoom):
        image = pygame.image.load(file).convert()
        return pygame.transform.smoothscale(image,zoom)



    def handleEvents(self):
        for event in pygame.event.get():
            card = self.board_.mp_.checkCursorIn(Point2(*pygame.mouse.get_pos()))
            if event.type == pygame.QUIT:
                self.running_ = False
            if event.type == pygame.MOUSEMOTION:
                mousePos = Point2(*event.pos)

                for c in self.board_.mp_.cards_:
                    c.isHovered_ = False
                if card:
                    card.isHovered_ = True

                if self.board_.mp_.draggedCard_:
                    try:
                        self.board_.mp_.draggedCard_.pos_ = mousePos+self.off_
                    except:
                        print('error')

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not card == self.board_.mp_.draggedCard_:
                    card.draggable_ = True
                    #self.board_.mp_.draggedCard_ = False
                    self.board_.mp_.draggedCard_ = card

                mousePos = Point2(*event.pos)
                self.off_ = card.pos_ - mousePos

            if event.type == pygame.MOUSEBUTTONUP:
                if self.board_.mp_.draggedCard_:
                    if self.board_.isInCentral(Point2(*event.pos)):
                        self.board_.getCentralClosest(Point2(*event.pos))
                    self.board_.mp_.draggedCard_.draggable_ = False
                    self.board_.mp_.draggedCard_.isHovered_ = False
                    self.board_.mp_.draggedCard_ = None



    def fill(self, color):
        self.screen_.fill(color)

    def flip(self):
        pygame.display.flip()


if __name__ == '__main__':
    #pygame.init()
    w = App()
