import pygame

from object import Object


class Explosion(Object):

    @staticmethod
    def charge_up(obj, game):
        super(Explosion, Explosion).charge_up(obj, game)
        obj.radius += obj.radius_speed
        if obj.charge >= 1.0:
            obj.active = False
            return
        if obj.charge >= 0.75:  # black is safe
            return
        for to_hit in game.get_colliding_units(obj):
            if to_hit == obj.source or to_hit in obj.already_hit:
                continue
            if obj.source:
                for func in obj.source.on_hit:
                    func(obj.source, game, to_hit)
            for func in to_hit.on_get_hit:
                func(to_hit, game, obj)
            obj.already_hit.add(to_hit)

    def __init__(self, pos, source, damage):
        super().__init__(pos, [0., 1.], 10.)
        self.charge_speed = 0.01
        self.radius_speed = 1.1
        self.source = source
        self.damage = damage
        self.already_hit = set()

    def draw(self, game, surface):
        color_intensity = 255.*(1. - self.charge) if self.charge < 0.75 else 0.
        if self.source == game.get_player():
            color = (0., 0., color_intensity)
        else:
            color = (color_intensity, 0., 0.)
        draw_pos = (int(self.pos[0]), int(self.pos[1]))
        pygame.draw.circle(surface, color, draw_pos, int(self.radius), 1)
