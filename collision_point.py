import pygame
import math
from random import random

from object import Object
import utils

class CollisionPoint(Object):
    def __init__(self, pos):
        super().__init__(pos, (0., 0.), 0.)
        self.on_get_hit = []

        def collide(obj, game):
            for to_hit in utils.colliding_objects(obj, game):
                v_to_hit = utils.cartesian2polar([ - to_hit.pos[0] + obj.pos[0], - to_hit.pos[1] + obj.pos[1]])
                v_speed = utils.cartesian2polar(to_hit.speed)
                if utils.dist(to_hit.speed, utils.polar2cartesian(v_speed)) > 1e-6:
                    raise AttributeError("Coordinate conversion failed: mismatch")
                v_speed[1] = 2.*v_to_hit[1] + math.pi - v_speed[1]
                to_hit.speed = utils.polar2cartesian(v_speed)

        self.on_update.append(collide)

    def draw(self, surface):
        if not self.active:
            return
        draw_pos = (int(self.pos[0]), int(self.pos[1]))
        pygame.draw.circle(surface, (255, 0, 0), draw_pos, int(1. + 4.*random()), 1)
