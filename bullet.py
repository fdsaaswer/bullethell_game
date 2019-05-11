import pygame

from object import Object

import utils


def hit(obj, game, one_time):
    for to_hit in game.get_colliding_units(obj):
        if to_hit == obj.source or to_hit in obj.ignored:
            continue
        for func in obj.on_hit:
            func(obj, game, to_hit)
        for func in to_hit.on_get_hit:
            func(to_hit, game, obj)
        if one_time:
            obj.is_active = False
        else:
            obj.ignored.add(to_hit)


class Bullet(Object):

    @staticmethod
    def position_shift(obj, game):
        super(Bullet, Bullet).position_shift(obj, game)
        if obj.charge >= 1.:
            hit(obj, game, True)

    def __init__(self, pos, speed, source, damage):
        super().__init__(pos, speed, 5.)
        self.charge_speed = 0.01 * utils.norm(speed)
        self.source = source
        self.damage = damage
        self.ignored = set()
        self.on_hit = []

    def draw(self, game, surface, erase=False):
        if erase:
            color = (255., 255., 255.)
        else:
            color_intensity = 150.*self.charge if self.charge < 1. else 255.
            color = (0., 0., color_intensity) if self.source == game.get_player() else (color_intensity, 0., 0.)
        draw_pos = (int(self.pos[0]), int(self.pos[1]))
        pygame.draw.circle(surface, color, draw_pos, int(self.radius), 0 if self.damage else 1)
