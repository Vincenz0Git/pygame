from pygame import transform
from GUI.myMath import Point2, Rec
from GUI.myCoord import *
import pygame.gfxdraw
import math


class Drawable:
    def __init__(self, pos, rot, zoom):
        # has a position, a rotation angle and a polygon hitbox
        self.rot_ = rot
        self.pos_ = pos
        self.polygon_ = None
        self.image_ = None
        self.zoom_ = zoom

    def getImage(self):
        z = transform.smoothscale(self.image_, self.zoom_)
        return transform.rotate(z, self.rot_)

    def draw(self, screen, hb):
        screen.blit(self.getImage(), self.pos_())
        if hb:
            pygame.gfxdraw.polygon(screen, self.hitBox()(), (255,0,0,255))

    def hitBox(self):
        # return Rec polygon hitbox
        zl = self.polygon_.zoom(self.zoom_)
        rl = zl.rotate(Point2(0,0),self.rot_*math.pi/180)
        return rl.translate(self.pos_)


class Deck(Drawable):
    def __init__(self, image, pos, rot, zoom):
        super().__init__(pos, rot, zoom)
        self.image_ = image
        self.polygon_ = Rec()
        self.polygon_.initFromSize(zoom)


class CentralZone(Rec):
    def __init__(self, sheet):
        # TODO class zone? with cards_ and rec?
        self.cards_ = []
        super().__init__(CENTRALZONE)
        #self.zoneCards_ = Rec(CENTRALZONE)
        self.d = Deck(sheet.getCardImage(4, 1, DrawableCard.CARDSIZE),Point2(160,180),0, DrawableCard.CARDSIZECENTER)
        self.initSomeCards(sheet)

    def initSomeCards(self, sheet):
        self.cards_.append(
         DrawableCard(sheet.getCardImage(2, 3, DrawableCard.CARDSIZE),Point2(290,185),5, DrawableCard.CARDSIZECENTER)
        )

    def draw(self, screen):
        pygame.gfxdraw.polygon(screen, self(), (0,0,255,255))
        screen.blit(self.d.getImage(), self.d.pos_())
        for card in self.cards_:
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

    def getCentralClosest(self, point):
        for card in self.cz_.cards_:
            print(card.hitBox().center()())


class PlayerZone(Rec):
    def __init__(self, points, sheet):
        super().__init__(points)
        self.cards_ = []

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
        #points = [Point2(150,550), Point2(850,550), Point2(850,900), Point2(150,900)]
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


class DrawableCard(Drawable):
    CARDSIZE = (120,180)
    CARDSIZECENTER = (105, 140)

    def __init__(self, image, pos, rot, zoom):
        # Call the parent class (Sprite) constructor
        Drawable.__init__(self, pos, rot, zoom)
        self.pos0_ = pos
        self.rot0_ = rot
        self.zoom0_ = zoom
        self.image_ = image
        self.polygon_ = Rec()
        self.polygon_.initFromSize(DrawableCard.CARDSIZE)
        self.draggable_ = False
        self.isHovered_ = False

    def resetTranforms(self):
        self.pos_ = self.pos0_
        self.rot_ = self.rot0_
        self.zoom_ = self.zoom0_

    def setPos0(self, pos):
        self.pos0_ = pos
        self.pos_ = pos

    def setrot0(self, rot):
        self.rot0_ = rot
        self.rot_ = rot


    def draw(self, screen, hb):
        # redefines the position/rotation/zoom, then call parent draw
        if (self.isHovered_ and not self.draggable_):
            self.pos_ = self.pos0_ - Point2(0, 50)
            self.zoom_ = (180, 240)
        elif self.draggable_:
            self.zoom_ = (180, 240)
        else:
            self.resetTranforms()

        super().draw(screen, hb)

    def isPointIn(self, point):
        return self.hitBox().isPointIn(point)
