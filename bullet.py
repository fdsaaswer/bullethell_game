import pygame

from object import Object
from explosion import Explosion
import utils

class Bullet(Object):

    @staticmethod
    def position_shift(obj, game):
        super(Bullet, Bullet).position_shift(obj, game)
        if obj.charge >= 1.:
            for to_hit in game.get_colliding_units(obj):
                for func in obj.on_hit:
                    func(obj, game)
                for func in to_hit.on_get_hit:
                    func(to_hit, game)

    def __init__(self, pos, speed):
        super().__init__(pos, speed, 5.)
        self.charge_speed = 0.01
        self.on_hit = []

        def disappear(obj, game):
            obj.active = False
        self.on_hit.append(disappear)

    def draw(self, surface):
        if not self.active:
            return
        color = (self.charge*150. if self.charge < 1. else 255., 0., 0.)
        draw_pos = (int(self.pos[0]), int(self.pos[1]))
        pygame.draw.circle(surface, color, draw_pos, int(self.radius), 0)
