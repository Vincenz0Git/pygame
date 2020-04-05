from pygame.sprite import Sprite
from GUI.mySprite import SpriteCards
from pygame import transform
from GUI.myMath import *
from operator import itemgetter

class Drawable(Sprite):
    def __init__(self, pos, rot):
        # has a position, a rotation angle and a polygon hitbox
        Sprite.__init__(self)
        self.rot_ = rot
        self.pos_ = pos
        self.polygon_ = None
        self.image_ = None


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

    def getImage(self):
        z = transform.smoothscale(self.image_, self.zoom_)
        return transform.rotate(z, self.rot_)

    def hitBox(self):
        # return Rec polygon hitbox
        zl = self.polygon_.zoom(self.zoom_)
        rl = zl.rotate(Point2(0,0),self.rot_*math.pi/180)

        return rl.translate(Point2(*self.pos_))

    def get3Vertices(self):
        # in a rectangle: # # # # # # # # # #
        # o ----------  # # # # # # # # # # #
        # | # # # # # | # # # # # # # # # # #
        # o ----------o # # # # # # # # # # #
        # Useful to check if a point is inside
        return itemgetter(0, 1, 3)(self.getPolygonTransformed())

    def isPointIn(self, point):
        return self.hitBox().isPointIn(point)
