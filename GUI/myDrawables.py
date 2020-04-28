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
