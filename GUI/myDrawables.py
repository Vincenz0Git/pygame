from pygame.sprite import Sprite
from mySprite import SpriteCards
from pygame import transform
from myCards import Card
from myMath import *
from operator import itemgetter

class Drawable(Sprite):
    def __init__(self, pos, rot):
        # has a position, a rotation angle and a polygon hitbox
        Sprite.__init__(self)
        self.rot_ = rot
        self.pos_ = pos
        self.polygon_ = [(0, 0),
                         (DrawableCard.SCALE[0], 0),
                         (DrawableCard.SCALE[0], DrawableCard.SCALE[1]),
                         (0, DrawableCard.SCALE[1])]
        self.image_ = None


class DrawableCard(Drawable):
    SCALE = (100, 140)

    def __init__(self, spritesheet, card, pos, rot):
        # Call the parent class (Sprite) constructor
        Drawable.__init__(self, pos, rot)

        print('aaa')
        self.image_ = spritesheet.getCardImage(card.color_, card.number_, DrawableCard.SCALE)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.draggable_ = False

    def getImage(self):
        return transform.rotate(self.image_, self.rot_)

    def getPolygonTransformed(self):
        rl = rotatelist(self.polygon_, (0, 0), self.rot_*math.pi/180)
        return translatelist(rl, self.pos_)

    def get3Vertices(self):
        # in a rectangle: # # # # # # # # # #
        # o ----------  # # # # # # # # # # #
        # | # # # # # | # # # # # # # # # # #
        # o ----------o # # # # # # # # # # #
        # Useful to check if a point is inside
        return itemgetter(0, 1, 3)(self.getPolygonTransformed())

    def isPointIn(self, point):
        return isin(point, self.get3Vertices() )



class DrawableCards:
    def __init__(self):
        pass
