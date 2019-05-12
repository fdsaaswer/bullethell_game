import pygame

from object import Object

import utils


class Hitter(Object):

    @staticmethod
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

    def __init__(self, pos, speed, radius, source, damage):
        super().__init__(pos, speed, radius)
        self.source = source
        self.damage = damage
        self.ignored = set()
        self.on_hit = []


class Bullet(Hitter):

    @staticmethod
    def position_shift(obj, game):
        super(Bullet, Bullet).position_shift(obj, game)
        if obj.charge >= 1.:
            super(Bullet, Bullet).hit(obj, game, True)

    def __init__(self, pos, speed, source, damage):
        super().__init__(pos, speed, 5., source, damage)
        self.charge_speed = 0.01 * utils.norm(speed)

    def draw(self, game, surface, erase=False):
        if erase:
            color_charge = (255., 255., 255.)
            color_internal = (255., 255., 255.)
        else:
            color_intensity_charge = 150.*self.charge if self.charge < 1. else 255.
            color_intensity_internal = 255. * max(0., 1. - self.damage)

            if self.source == game.get_player():
                color_charge = (0., 0., color_intensity_charge)
                color_internal = (color_intensity_internal, color_intensity_internal, 255.)
            else:
                color_charge = (color_intensity_charge, 0., 0.)
                color_internal = (255., color_intensity_internal, color_intensity_internal)

        draw_pos = (int(self.pos[0]), int(self.pos[1]))
        pygame.draw.circle(surface, color_internal, draw_pos, int(self.radius), 0)
        pygame.draw.circle(surface, color_charge, draw_pos, int(self.radius), 1)


class Explosion(Hitter):

    @staticmethod
    def charge_up(obj, game):
        super(Explosion, Explosion).charge_up(obj, game)
        obj.radius += obj.radius_speed
        if obj.charge >= 1.0:
            obj.is_active = False
            return
        if obj.charge >= 0.75:  # black is safe
            return
        super(Explosion, Explosion).hit(obj, game, False)

    def __init__(self, pos, source, damage):
        super().__init__(pos, [0., 1.], 10., source, damage)
        self.charge_speed = 0.01
        self.radius_speed = 1.1

    def draw(self, game, surface, erase):
        if erase:
            color = (255., 255., 255.)
        else:
            color_intensity = 255.*(1. - self.charge) if self.charge < 0.75 else 0.
            if self.source == game.get_player():
                color = (0., 0., color_intensity)
            else:
                color = (color_intensity, 0., 0.)
        draw_pos = (int(self.pos[0]), int(self.pos[1]))
        pygame.draw.circle(surface, color, draw_pos, int(self.radius), 1)
