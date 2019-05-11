import math
from random import random


class with_chance:
    def __init__(self, chance):
        self.chance = chance

    def __call__(self, f):
        def wrapped_f(*args):
            if random() < self.chance:
                f(*args)

        return wrapped_f


def norm(vector):
    return math.sqrt(vector[0] ** 2 + vector[1] ** 2)

def normalize(vector, rho=1):
    a = vector[0]
    b = vector[1]
    norm = math.sqrt(a ** 2 + b ** 2)
    if norm == 0.:
        return vector
    return [a*rho/norm, b*rho/norm]


def dist(pos_1, pos_2):
    a = pos_1[0] - pos_2[0]
    b = pos_1[1] - pos_2[1]
    return math.sqrt(a ** 2 + b ** 2)


def cartesian2polar(coord):
    phi = math.atan2(coord[1], coord[0])
    rho = math.sqrt(coord[0] ** 2 + coord[1] ** 2)
    return [rho, phi]


def polar2cartesian(coord):
    x = coord[0] * math.cos(coord[1])
    y = coord[0] * math.sin(coord[1])
    return [x, y]


def collide(obj, anchor):  # modifies obj.speed
    approach = cartesian2polar([anchor[0] - obj.pos[0], anchor[1] - obj.pos[1]])
    speed = cartesian2polar(obj.speed)
    if dist(obj.speed, polar2cartesian(speed)) > 1e-6:
        raise AttributeError("Coordinate conversion failed: mismatch")
    if abs(speed[1] - approach[1]) > 0.5 * math.pi:
        speed[1] = approach[1] + math.pi
        speed[0] *= 1.25
    else:
        speed[1] = 2. * approach[1] + math.pi - speed[1]
        speed[0] *= 0.8
    obj.speed = polar2cartesian(speed)


def shift_to(value, target, step):
    if value < target:
        return max(value + step, target)
    else:
        return min(value - step, target)
