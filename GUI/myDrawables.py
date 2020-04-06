from pygame import transform
from GUI.myMath import Point2, Rec
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


class Board:
    def __init__(self, sheet):
        self.centralCards_ = []
        self.zoneCards_ = Rec([Point2(280,180), Point2(800,180), Point2(800,330), Point2(280,330)])
        self.zonePlays_ = Rec([Point2(280,330), Point2(800,330), Point2(800,480), Point2(280,480)])
        self.d = Deck(sheet.getCardImage(4, 1, DrawableCard.CARDSIZE),Point2(160,180),0, DrawableCard.CARDSIZECENTER)
        self.initSomeCards(sheet)

    def initSomeCards(self, sheet):
        self.centralCards_.append(
         DrawableCard(sheet.getCardImage(2, 3, DrawableCard.CARDSIZE),Point2(290,185),5, DrawableCard.CARDSIZECENTER)
        )

    def draw(self, screen):
        pygame.gfxdraw.polygon(screen, self.zoneCards_(), (0,0,255,255))
        pygame.gfxdraw.polygon(screen, self.zonePlays_(), (0,0,255,255))
        screen.blit(self.d.getImage(), self.d.pos_())
        for card in self.centralCards_:
            card.draw(screen, True)


class MainPlayer:
    def __init__(self, pos, rot, size, sheet):
        self.cards_ = []
        self.handZone_ = Rec()
        self.handZone_.initFromSize(size)
        self.pos_ = pos
        self.rot_ = rot
        self.draggedCard_ = None
        self.hoveredCard_ = None
        self.initSomeCards(sheet)

    def checkCursorIn(self, cursor):
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
        l = [(1, 2), (2, 4), (3, 8), (2, 5), (0, 3), (1, 10), (3, 0), (2, 5), (0, 3), (1, 10), (3, 0)]
        l1 = [(1, 2), (2, 4), (3, 8), (2, 5), (0, 3), (1, 10)]
        l1 = [(1, 2), (2, 4)]

        for i, (a,b) in enumerate(l):

            w = (len(l)-1)*DrawableCard.CARDSIZE[0]/2

            rotmax = 3*len(l)
            if rotmax > 20:
                rotmax = 20

            if w > self.handZone_.size_[0]:
                w = self.handZone_.size_[0]

            boardLeft = self.pos_.x_ + (self.handZone_.width() - w)/2
            boardRight = self.pos_.x_ + self.handZone_.width() - (self.handZone_.width() - w)/2

            if len(l)%2 == 0:
                boardLeft -= DrawableCard.CARDSIZE[0]
                boardRight -= DrawableCard.CARDSIZE[0]
            else:
                boardLeft -= DrawableCard.CARDSIZE[0]/2
                boardRight -= DrawableCard.CARDSIZE[0]/2

            rot = rotmax + i/(len(l)-1)*(-rotmax - rotmax)
            posx = boardLeft+i/(len(l)-1)*(boardRight - boardLeft)
            t = rotmax/20
            posy = self.pos_.y_+t*self.handZone_.size_[1]/10
            pos = (posx, posy)

            self.cards_.append(
             DrawableCard(sheet.getCardImage(a, b, DrawableCard.CARDSIZE),Point2(*pos),rot,DrawableCard.CARDSIZE)
            )

            if i > 0:
                posLeft1 = self.cards_[i-1].hitBox().points_[0]
                posLeft2 = self.cards_[i-1].hitBox().points_[1]
                posRight = self.cards_[i].hitBox().points_[0]

                t = -(posLeft1.x_ - posRight.x_)/DrawableCard.CARDSIZE[0]
                posLeft = posLeft1.y_*(1-t) + posLeft2.y_*t
                offsety = posLeft - posRight.y_

                self.cards_[i].pos0_ += Point2(0, offsety)
                self.cards_[i].pos_ = self.cards_[i].pos0_


    def draw(self, screen):
        zone = self.handZone_.rotate(Point2(0,0), self.rot_).translate(self.pos_)
        pygame.gfxdraw.polygon(screen, zone(), (0,255,0,255))
        hoveredcard = None
        for card in self.cards_:
            if not card.isHovered_:
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
