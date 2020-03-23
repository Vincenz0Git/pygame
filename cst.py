from enum import Enum
from itertools import product


class Color(Enum):
    RED     = 0
    GREEN   = 1
    BLUE    = 2
    YELLOW  = 3


class Number(Enum):
    TEN     = 10
    NINE    = 9
    EIGHT   = 8
    SEVEN   = 7
    SIX     = 6
    FIVE    = 5
    FOUR    = 4
    THREE   = 3
    TWO     = 2
    ONE     = 1
    JOKER   = 0


class Bonus(Enum):
    COLOR1 = 0
    COLOR2 = 1
    NONE = 2


l3of = [Number.ONE, Number.THREE, Number.FOUR, Number.FIVE, Number.TWO]*3
l2of = [Number.SIX, Number.SEVEN, Number.EIGHT, Number.NINE,
        Number.TEN, Number.JOKER]*2

lnum = l3of + l2of

Composition = product(Color, lnum)
