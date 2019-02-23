import pygame

from object import Object


class Bullet(Object):

    @staticmethod
    def position_shift(obj, game):
        super(Bullet, Bullet).position_shift(obj, game)
        if obj.charge >= 1.:
            for to_hit in game.get_colliding_units(obj):
                obj.active = False
                if obj.source:
                    for func in obj.source.on_hit:
                        func(obj, game, to_hit)
                for func in to_hit.on_get_hit:
                    func(to_hit, game, obj)

    def __init__(self, pos, speed, source, damage):
        super().__init__(pos, speed, 5.)
        self.charge_speed = 0.01
        self.source = source
        self.damage = damage

    def draw(self, surface):
        if not self.active:
            return
        color = (self.charge * 150. if self.charge < 1. else 255., 0., 0.)
        draw_pos = (int(self.pos[0]), int(self.pos[1]))
        pygame.draw.circle(surface, color, draw_pos, int(self.radius), 0)
