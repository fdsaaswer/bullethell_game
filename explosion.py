import pygame

from object import Object
import utils

class Explosion(Object):
    def __init__(self, obj):
        super().__init__(obj.pos, [0., 1.], 10.)

        def charge_up(obj, game):
            if obj.charge < 1.5:
                obj.charge += 0.01
                self.radius += 1.1

                to_hit_units = [o for o in game.units
                                if o.active and o != obj and utils.dist(o.pos, obj.pos) < (o.radius + obj.radius)]
                for to_hit in to_hit_units:
                    to_hit.active = False
                    game.effects.append(Explosion(to_hit))
            else:
                obj.active = False
        self.charge = 0
        self.on_update = [charge_up]

    def draw(self, surface):
        if not self.active:
            return
        color = (255. - self.charge*200. if self.charge < 1. else 0., 0., 0.)
        draw_pos = (int(self.pos[0]), int(self.pos[1]))
        pygame.draw.circle(surface, color, draw_pos, int(self.radius), 1)
