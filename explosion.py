import pygame

from object import Object


class Explosion(Object):

    @staticmethod
    def charge_up(obj, game):
        super(Explosion, Explosion).charge_up(obj, game)
        obj.radius += 1.1
        if obj.charge >= 1.0:
            obj.active = False
            return
        if obj.charge >= 0.75:  # black is safe
            return

        try:
            obj.already_hit
        except AttributeError:
            obj.already_hit = set()

        for to_hit in game.get_colliding_units(obj):
            if to_hit in obj.already_hit:
                continue
            obj.already_hit.add(to_hit)
            for func in to_hit.on_get_hit:
                func(to_hit, game)

    def __init__(self, obj):
        super().__init__(obj.pos, [0., 1.], 10.)
        self.charge_speed = 0.01

    def draw(self, surface):
        if not self.active:
            return
        color = (255.*(1. - self.charge) if self.charge < 0.75 else 0., 0., 0.)
        draw_pos = (int(self.pos[0]), int(self.pos[1]))
        pygame.draw.circle(surface, color, draw_pos, int(self.radius), 1)
