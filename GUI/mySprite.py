import pygame


class Spritesheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert_alpha()
        #print('Unable to load spritesheet image:', filename)

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            #image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey) for rect in rects]
    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)


class SpriteCards(Spritesheet):
    H = 530
    W = 362
    def __init__(self,filename):
        super().__init__(filename)

    def getRectangle(self,color,number):
        # get Rectangle type object for card of color and number
        # Rectangle: offsetx,offsety,width,height
        return (number*SpriteCards.W-1,color*SpriteCards.H,
                                SpriteCards.W,SpriteCards.H)

    def getCardImage(self,color,number,scale):
        # get Surface object with image of card
        image = self.image_at(self.getRectangle(color,number))
        return pygame.transform.smoothscale(image,scale)
