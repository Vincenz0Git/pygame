from pygame.sprite import Sprite
from myMath import *
from operator import itemgetter
from mySprite import Number,Color
from random import shuffle


class Card:
    def __init__(self,color,number):
        self.color_ = color
        self.number_ = number
    def __repr__(self):
        return "{} {}".format(self.color_,self.number_)


class DrawableCard(Sprite,Card):
    SCALE = (100,140)
    def __init__(self, color, number, pos, rot):
        # Call the parent class (Sprite) constructor
        Sprite.__init__(self)
        Card.__init__(self,color,number)

        self.rot_ = rot
        self.pos_ = pos

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image_ = None

        self.polygon_ = [(0, 0),
                         (DrawableCard.SCALE[0], 0),
                         (DrawableCard.SCALE[0], DrawableCard.SCALE[1]),
                         (0, DrawableCard.SCALE[1])]

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.draggable_ = False

    def getImage(self, spritesheet):
        self.image_ = spritesheet.getCardImage(self.color_,self.number_,DrawableCard.SCALE)

    def getPolygonTransformed(self):
        rl = rotatelist(self.polygon_, (0, 0), self.rot_*math.pi/180)
        return translatelist(rl, self.pos_)

    def get3Vertices(self):
        return itemgetter(0,1,3)(self.getPolygonTransformed())

    def isPointIn(self,point):
        return isin(point,self.get3Vertices())

    def update(self):
        pass


class Deck:
    def __init__(self):
        self.cards_ = []
        self.ncards_ = 108
        self.generateDeck()
        self.shuffle()
        for i in range(7):
            print(self.cards_[i])

    def generateCards(self,color,number,repetition):
        # generate "repetition" cards with "number" and "color"
        for i in range(repetition):
            self.cards_.append(Card(color,number))

    def generateDeck(self):
        l3of = [Number.ONE,Number.THREE,Number.FOUR,Number.FIVE,Number.TWO]
        l2of = [Number.SIX,Number.SEVEN,Number.EIGHT,Number.NINE,Number.TEN,Number.JOKER]
        for col in list(Color):
            for n in l3of:
                self.generateCards(col,n,3)
            for n in l2of:
                self.generateCards(col,n,2)

    def shuffle(self):
        shuffle(self.cards_)

    def takeTopCard(self):
        self.ncards_ -= 1
        return self.cards_.pop()
