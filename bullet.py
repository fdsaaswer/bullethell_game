import pygame

from object import Object
from explosion import Explosion
import utils

class Bullet(Object):

    @staticmethod
    def position_shift(obj, game):
        if obj.charge < 1.:
            super(Bullet, Bullet).position_shift(obj, game)
        else:
            new_pos = [obj.pos[idx] + obj.speed[idx] for idx, ignored in enumerate(obj.pos)]
            to_hit_units = [o for o in game.units
                            if o.active and o != obj and utils.dist(o.pos, new_pos) < (o.radius + obj.radius)]
            for to_hit_obj in to_hit_units:
                for func in obj.on_hit:
                    func(obj, game)
                for func in to_hit_obj.on_get_hit:
                    func(to_hit_obj, game)
                break
            else:
                obj.pos = new_pos

    def __init__(self, pos, speed, radius):
        super().__init__(pos, speed, radius)
        self.on_hit = []

        def disappear(obj, game):
            obj.active = False
        self.on_hit.append(disappear)

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
        pygame.draw.circle(surface, color, draw_pos, int(self.radius), 0)
