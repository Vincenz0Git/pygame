from pygame.sprite import Sprite
from GUI.mySprite import SpriteCards
from pygame import transform
from GUI.myMath import *
from operator import itemgetter
import pygame.gfxdraw

class Drawable(Sprite):
    def __init__(self, pos, rot):
        # has a position, a rotation angle and a polygon hitbox
        Sprite.__init__(self)
        self.rot_ = rot
        self.pos_ = pos
        self.polygon_ = None
        self.image_ = None

class MainPlayer:
    def __init__(self, pos, rot, size, sheet):
        self.cards_ = []
        self.handZone_ = Rec()
        self.handZone_.initFromSize(size)
        self.pos_ = pos
        self.rot_ = rot
        self.initSomeCards(sheet)

    def checkCursorIn(self, cursor):
        listIn = []
        for card in self.cards_:
            if card.hitBox().isPointIn(cursor):
                print(card.pos_[0])
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

            boardLeft = self.pos_.x_ + (self.handZone_.size_[0] - w)/2
            boardRight = self.pos_.x_ + self.handZone_.size_[0] - (self.handZone_.size_[0] - w)/2

            if len(l)%2 == 0:
                boardLeft -= DrawableCard.CARDSIZE[0]
                boardRight -= DrawableCard.CARDSIZE[0]
            else:
                boardLeft -= DrawableCard.CARDSIZE[0]/2
                boardRight -= DrawableCard.CARDSIZE[0]/2

            midx = (boardLeft + boardRight)/2
            rot = rotmax + i/(len(l)-1)*(-rotmax - rotmax)
            posx = boardLeft+i/(len(l)-1)*(boardRight - boardLeft)
            t = rotmax/20
            print(t)
            posy = self.pos_.y_+t*self.handZone_.size_[1]/10
            pos = (posx, posy)

            self.cards_.append(
             DrawableCard(sheet.getCardImage(a, b, DrawableCard.CARDSIZE),pos,rot)
            )

            if i > 0:
                posLeft1 = self.cards_[i-1].hitBox().points_[0]
                posLeft2 = self.cards_[i-1].hitBox().points_[1]
                posRight = self.cards_[i].hitBox().points_[0]

                t = -(posLeft1.x_ - posRight.x_)/DrawableCard.CARDSIZE[0]
                posLeft = posLeft1.y_*(1-t) + posLeft2.y_*t
                offsety = posLeft - posRight.y_

                self.cards_[i].pos_ = (self.cards_[i].pos_[0], self.cards_[i].pos_[1]+offsety)
                self.cards_[i].polygon_.translate(Point2(offsety,offsety))


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

    def __init__(self, image, pos, rot):
        # Call the parent class (Sprite) constructor
        Drawable.__init__(self, pos, rot)
        self.image_ = image
        self.zoom_ = DrawableCard.CARDSIZE
        self.polygon_ = Rec()
        self.polygon_.initFromSize(DrawableCard.CARDSIZE)
        # [(0, 0),
        #                  (DrawableCard.CARDSIZE[0], 0),
        #                  (DrawableCard.CARDSIZE[0], DrawableCard.CARDSIZE[1]),
        #                  (0, DrawableCard.CARDSIZE[1])]
        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.draggable_ = False
        self.isHovered_ = False

    def draw(self, screen, hb):
        pos = None
        if not self.isHovered_:
            pos = self.pos_
        else:
            pos = (self.pos_[0], self.pos_[1]-50)

        cpos = self.pos_
        self.pos_=pos
        screen.blit(self.getImage(), pos)
        if hb:
            pygame.gfxdraw.polygon(screen, self.hitBox()(), (255,0,0,255))
        self.pos_ = cpos

    def getImage(self):
        z = transform.smoothscale(self.image_, self.zoom_)
        return transform.rotate(z, self.rot_)

    def hitBox(self):
        # return Rec polygon hitbox
        zl = self.polygon_.zoom(self.zoom_)
        rl = zl.rotate(Point2(0,0),self.rot_*math.pi/180)

        return rl.translate(Point2(*self.pos_))

    def isPointIn(self, point):
        return self.hitBox().isPointIn(point)
