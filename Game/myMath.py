import math

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) + math.sin(angle) * (py - oy)
    qy = oy - math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


def sp(p1,p2):
    return p1[0]*p2[0]+p1[1]*p2[1]

def isin(point,list):
    p1 = list[0]
    l = [(el[0]-p1[0],el[1]-p1[1]) for el in list[1:]]
    v = (point[0]-p1[0],point[1]-p1[1])
    return 0 < sp(v,l[0]) < sp(l[0],l[0]) and 0 < sp(v,l[1]) < sp(l[1],l[1])


def translatelist(list,t):
    return [(el[0]+t[0],el[1]+t[1]) for el in list]

def rotatelist(list,origin,angle):
    l = []
    minx = 0
    miny = 0
    for el in list:
        new_p = rotate(origin,el,angle)
        l.append(new_p)
        if new_p[0]<minx:
            minx = new_p[0]
        if new_p[1]<miny:
            miny = new_p[1]

    return [(el[0]-minx*(minx<0),el[1]-miny*(miny<0)) for el in l]
