import pygame

from object import Object
import utils

class Explosion(Object):
    CHARGE_MAX = 1.

    def __init__(self, obj):
        super().__init__(obj.pos, [0., 1.], 10.)

        def charge_up(obj, game):
            obj.charge += 0.01
            self.radius += 1.1
            if obj.charge >= self.CHARGE_MAX*1.5:
                obj.active = False
                return
            if obj.charge >= self.CHARGE_MAX: # black is safe
                return

            try:
                obj.already_hit
            except AttributeError:
                obj.already_hit = set()

            for to_hit in utils.colliding_objects(obj, game):
                if to_hit in obj.already_hit:
                    continue
                obj.already_hit.add(to_hit)
                for func in to_hit.on_get_hit:
                    func(to_hit, game)

        self.charge = 0
        self.on_update.append(charge_up)

    def draw(self, surface):
        if not self.active:
            return
        color = (255. - self.charge*200. if self.charge < self.CHARGE_MAX else 0., 0., 0.)
        draw_pos = (int(self.pos[0]), int(self.pos[1]))
        pygame.draw.circle(surface, color, draw_pos, int(self.radius), 1)
