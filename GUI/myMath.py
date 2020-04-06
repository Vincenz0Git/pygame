import math

from operator import itemgetter


class Point2:
    def __init__(self,x,y):
        self.x_ = x
        self.y_ = y

    def rotate(self, origin, angle):
        """
        Rotate a point counterclockwise by a given angle around a given origin.

        The angle should be given in radians.
        """
        ox, oy = origin()

        qx = ox + math.cos(angle) * (self.x_ - ox) + math.sin(angle) * (self.y_ - oy)
        qy = oy - math.sin(angle) * (self.x_ - ox) + math.cos(angle) * (self.y_ - oy)

        return Point2(qx,qy)

    def norm(self):
        return math.sqrt(self.x_**2 + self.y_**2)

    def __mul__(self, other):
        try:
            return self.x_*other.x_ + self.y_*other.y_
        except AttributeError:
            return Point2(other*self.x_, other*self.y_)

    def __truediv__(self,other):
        return Point2(self.x_/other, self.y_/other)

    def __add__(self, other):
        return Point2(self.x_ + other.x_, self.y_ + other.y_)

    def __sub__(self, other):
        return Point2(self.x_ - other.x_, self.y_ - other.y_)

    def __call__(self):
        return self.x_, self.y_


class Polygon:
    def __init__(self, points = []):
        self.points_ = points
        self.currentPoints_ = points

    def translate(self, translation):
        self.currentPoints_ = [point+translation for point in self.points_]
        return self.currentPoints_

    def zoom(self, zoom):
        self.currentPoints_ = [Point2(point.x_ * zoom.x_,point.y_*zoom.y_) for point in self.points_]
        return self.currentPoints_

    def rotate(self, origin, angle):

        l = []
        minx = 0
        miny = 0
        for point in self.points_:
            new_p = point.rotate(origin,angle)
            l.append(new_p)
            if new_p.x_ < minx:
                minx = new_p.x_
            if new_p.y_ < miny:
                miny = new_p.y_

        self.currentPoints_ = [Point2(el.x_-minx*(minx<0),el.y_-miny*(miny<0)) for el in l]
        return self.currentPoints_

    def __call__(self, formatPoint2):
        if formatPoint2:
            return [Point2(point.x_,point.y_) for point in self.points_]
        else:
            return [(point.x_,point.y_) for point in self.points_]


class Rec(Polygon):
    def __init__(self, points = []):
        super().__init__(points)
        try:
            self.size_ = ((points[0]-points[1]).norm(),(points[0]-points[3]).norm())
        except:
            self.size_ = (0,0)

    def initFromSize(self, size):
        self.points_ = [ Point2(0,0),
                         Point2(size[0],0),
                         Point2(size[0],size[1]),
                         Point2(0,size[1]) ]

        self.currentPoints_ = self.points_

        self.size_ = size



    def center(self):
        return (self.points_[0] + self.points_[2])/2

    def rotate(self, origin, angle):
        return Rec(super().rotate(origin, angle))

    def translate(self, translation):
        return Rec(super().translate(translation))

    def zoom(self, pzoom):
        # pzoom is the new size of the card
        return Rec(super().zoom(Point2(pzoom[0]/self.size_[0], pzoom[1]/self.size_[1])))

    def get3Vertices(self):
        # in a rectangle: # # # # # # # # # #
        # o ----------  # # # # # # # # # # #
        # | # # # # # | # # # # # # # # # # #
        # o ----------o # # # # # # # # # # #
        # Useful to check if a point is inside
        return itemgetter(0, 1, 3)(self.points_)

    def isPointIn(self, target):
        # check if target Point2 is in the rectangle
        points = self.get3Vertices()
        topleft = points[0]
        l = [ point - topleft for point in points[1:]]
        v = target - topleft
        return 0 < v*l[0] < l[0]*l[0] and 0 < v*l[1] < l[1]*l[1]

    def __call__(self):
        return [point() for point in self.points_]
