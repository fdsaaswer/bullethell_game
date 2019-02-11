import math
from random import random


class with_chance():
    def __init__(self, chance):
        self.chance = chance
    def __call__(self, f):
        def wrapped_f(*args):
            if random() < self.chance:
                f(*args)
        return wrapped_f


def dist(pos_1, pos_2):
    a = pos_1[0] - pos_2[0]
    b = pos_1[1] - pos_2[1]
    return math.sqrt(a*a + b*b)


def colliding_objects(obj, game):
    return [o for o in game.units if o.active and o != obj and dist(o.pos, obj.pos) < (o.radius + obj.radius)]


def cartesian2polar(coord):
    phi = math.atan2(coord[1], coord[0])
    rho = math.sqrt(coord[0] ** 2 + coord[1] ** 2)
    return [rho, phi]


def polar2cartesian(coord):
    x = coord[0] * math.cos(coord[1])
    y = coord[0] * math.sin(coord[1])
    return [x, y]
