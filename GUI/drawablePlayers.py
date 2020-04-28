from GUI.myMath import Rec, Point2
from GUI.myDrawables import DrawableCard
import math
from GUI.myCoord import MPZONE
import pygame

class PlayerZone(Rec):
    def __init__(self, points, sheet):
        super().__init__(points)
        self.cards_ = []

    def removeCard(self, card):
        for i in range(len(self.cards_)):
            if self.cards_[i] == card:
                self.cards_.pop(i)
                break

    def topLeft(self):
        return self.points_[0]

    def getPosFromRelative(self, point):
        return self.topLeft()+point.x_*self.ex() + point.y_*self.ey()

    def getPosFromAbs(self, point):
        return point - self.topLeft()

    def computeCardPos(self, nCards):
        w = (nCards-1)*DrawableCard.CARDSIZE[0]/2

        rotmax = 2*nCards
        if rotmax > 15:
            rotmax = 15

        if w > self.size_[0]:
            w = self.size_[0]

        boardLeft = self.getPosFromRelative(Point2((self.width() - w)/2,0))
        boardRight = self.getPosFromRelative(Point2(self.width() - (self.width() - w)/2,0))

        boardLeft -= DrawableCard.CARDSIZE[0]/2*self.ex()
        boardRight -= DrawableCard.CARDSIZE[0]/2*self.ex()

        posy = 50
        overlap = DrawableCard.CARDSIZE[0]-w/(nCards-1)
        rot = []
        pos = []

        m = 10000

        for i in range(nCards):
            rot.append(rotmax + i/(nCards-1)*(-rotmax - rotmax))
            relpos = self.getPosFromAbs(boardLeft) + i/(nCards-1)*(boardRight - boardLeft)
            prevoff = math.tan(rot[-1]*math.pi/180)*overlap
            if i > 0:
                posy -= math.sin(rot[-1]*math.pi/180)*DrawableCard.CARDSIZE[0] - prevoff
            relpos += Point2(0,posy)

            pos.append(self.getPosFromRelative(relpos))
            if relpos.y_ < m:
                m = relpos.y_

        pos = [el - Point2(0,m) for el in pos]

        return pos, rot




class MainPlayerZone(PlayerZone):
    def __init__(self, sheet):
        super().__init__(MPZONE, sheet)
        self.draggedCard_ = None
        self.hoveredCard_ = None
        self.initSomeCards(sheet)

    def checkCursorIn(self, cursor):
        if self.draggedCard_:
            return None
        listIn = []
        for card in self.cards_:
            if card.hitBox().isPointIn(cursor):
                listIn.append(card)

        if len(listIn) == 1:
            return listIn[0]
        elif len(listIn) > 1:
            distances = []
            for card in listIn:
                pc = card.hitBox().center()
                distances.append((pc-cursor).norm())
            return listIn[distances.index(min(distances))]


    def initSomeCards(self, sheet):
        l = [(1, 2), (2, 4), (3, 8), (2, 5), (0, 3), (1, 10), (3, 0), (2, 5), (0, 3), (1, 10), (3, 0), (2, 2), (3, 4), (0, 5)]
        l1 = [(1, 2), (2, 4), (3, 8), (2, 5), (0, 3), (1, 10), (2,1)]
        l1 = [(1, 2), (2, 4)]

        pos, rot = self.computeCardPos(len(l))

        for i in range(len(l)):
            self.cards_.append(
             DrawableCard(sheet.getCardImage(l[i][0], l[i][1], DrawableCard.CARDSIZE),pos[i],rot[i],DrawableCard.CARDSIZE)
            )

    def draw(self, screen):
        pygame.gfxdraw.polygon(screen, self(), (0,255,0,255))
        hoveredcard = None
        ncards = len(self.cards_) - (not self.draggedCard_ == None)
        pos, rot = self.computeCardPos(ncards)

        #TODO probably not necessary to update each time
        i = 0
        for card in self.cards_:
            if not card == self.draggedCard_:
                card.setPos0(pos[i])
                card.setrot0(rot[i])
                i+=1

        for card in self.cards_:
            if not card.isHovered_ and not card.draggable_:
                card.draw(screen,True)
            else:
                hoveredcard = card
        if hoveredcard:
            hoveredcard.draw(screen,True)
