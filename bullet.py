import pygame

from object import Object


class Bullet(Object):

    @staticmethod
    def position_shift(obj, game):
        super(Bullet, Bullet).position_shift(obj, game)
        if obj.charge >= 1.:
            for to_hit in game.get_colliding_units(obj):
                if to_hit == obj.source:
                    continue
                if obj.source:
                    for func in obj.source.on_hit:  # TODO: apply on_hit for both bullet and source
                        func(obj.source, game, to_hit)
                for func in to_hit.on_get_hit:
                    func(to_hit, game, obj)
                obj.is_active = False

    def __init__(self, pos, speed, source, damage):
        super().__init__(pos, speed, 5.)
        self.charge_speed = 0.01
        self.source = source
        self.damage = damage

    def draw(self, game, surface):
        color_intensity = 150.*self.charge if self.charge < 1. else 255.
        color = (0., 0., color_intensity) if self.source == game.get_player() else (color_intensity, 0., 0.)
        draw_pos = (int(self.pos[0]), int(self.pos[1]))
        pygame.draw.circle(surface, color, draw_pos, int(self.radius), 0 if self.damage else 1)
