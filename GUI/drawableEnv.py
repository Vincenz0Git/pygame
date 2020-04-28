import pygame

from GUI.myMath import Rec, Point2
from GUI.myCoord import CENTRALZONE
from GUI.myDrawables import DrawableCard, Deck
from GUI.drawablePlayers import MainPlayerZone

from random import random


class CentralZone(Rec):
    def __init__(self, sheet):
        # TODO class zone? with cards_ and rec?
        self.cards_ = []
        super().__init__(CENTRALZONE)
        self.deck_ = Deck(sheet.getCardImage(4, 1, DrawableCard.CARDSIZE),Point2(160,180),0, DrawableCard.CARDSIZECENTER)
        self.initSomeCards(sheet)

    def computePos(self, nCards):
        nMax = self.width()//130
        if nCards < nMax-1:
            return [Point2(290+i*130,185) for i in range(nCards)]
        else:
            return [Point2(290+i*self.width()//(nCards+1), 185) for i in range(nCards)]

    def initSomeCards(self, sheet):
        l = [(2,3),(3,6),(1,2),(0,0),(1,9), (2,5), (3, 10)]
        for i, el in enumerate(l):
            self.addCard(
             i,
             DrawableCard(sheet.getCardImage(el[0], el[1], DrawableCard.CARDSIZE),Point2(0,0),10*(random()-0.5), DrawableCard.CARDSIZECENTER)
            )

        self.addPlay(
          DrawableCard(sheet.getCardImage(0, 0, DrawableCard.CARDSIZE),Point2(0,0),10*(random()-0.5), DrawableCard.CARDSIZECENTER),
          0
        )

        self.addPlay(
          DrawableCard(sheet.getCardImage(2, 3, DrawableCard.CARDSIZE),Point2(0,0),10*(random()-0.5), DrawableCard.CARDSIZECENTER),
          0
        )
        self.removePile(1)

    def removePile(self, index):
        # TODO self.cards_ as dictionary, lot of debugg here
        self.cards_.pop(index)
        newpos = self.computePos(len(self.cards_))
        for i, cards in enumerate(self.cards_):
            for card in cards:
                card.setPos0(newpos[i])

    def addCard(self, index, card):
        self.cards_.append([card])
        newpos = self.computePos(len(self.cards_))
        for i, cards in enumerate(self.cards_):
            cards[0].setPos0(newpos[i])

    def addPlay(self, card, index):
        topos = self.cards_[index][0].pos_ + Point2(0,DrawableCard.CARDSIZECENTER[1]+DrawableCard.CARDSIZECENTER[1]/4*(len(self.cards_[index])-1))
        card.setPos0(topos)
        self.cards_[index].append(card)


    def draw(self, screen):
        pygame.gfxdraw.polygon(screen, self(), (0,0,255,255))
        screen.blit(self.deck_.getImage(), self.deck_.pos_())
        for cards in self.cards_:
            for card in cards:
                card.draw(screen, True)


class Board:
    def __init__(self, sheet):
        self.mp_ = MainPlayerZone(sheet)
        self.cz_ = CentralZone(sheet)

    def draw(self, screen):
        self.cz_.draw(screen)
        self.mp_.draw(screen)

    def isInCentral(self, point):
        return self.cz_.isPointIn(point)

    def mpToCentral(self,card):
        self.cz_.addCard(card)
        self.mp_.removeCard(card)

    def getCentralClosest(self, point):
        min = 1000
        imin = 0
        for i, cards in enumerate(self.cz_.cards_):
            dist = (point-cards[0][1].hitBox().center()).norm()
            if dist < min:
                min = dist
                imin = i

        print(self.cz_.cards_.keys())
