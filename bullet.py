import pygame

from object import Object
from object import Explosion
import utils

class Bullet(Object):

    @staticmethod
    def position_shift(obj, game):
        if obj.charge < 1.:
            super(Bullet, Bullet).position_shift(obj, game)
        else:
            new_pos = [obj.pos[idx] + obj.speed[idx] for idx, ignored in enumerate(obj.pos)]
            for to_hit in game.units:
                if to_hit != obj and utils.dist(to_hit.pos, new_pos) < (to_hit.radius + obj.radius):
                    for func in obj.on_hit:
                        func(obj, game)
                    obj.active = False
                    to_hit.active = False
                    game.effects.append(Explosion(to_hit))
                    break
            else:
                obj.pos = new_pos

    def __init__(self, pos, speed, radius):
        super().__init__(pos, speed, radius)
        self.on_hit = []

        def charge_up(obj, game):
            if obj.charge < 1.:
                obj.charge += 0.01
        self.charge = 0
        self.on_update.append(charge_up)


    def draw(self, surface):
        if not self.active:
            return
        color = (self.charge*100. if self.charge < 1. else 255., 0., 0.)
        draw_pos = (int(self.pos[0]), int(self.pos[1]))
        pygame.draw.circle(surface, color, draw_pos, self.radius, 0)
