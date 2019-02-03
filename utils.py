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