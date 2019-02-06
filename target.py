import pygame
from random import random

from object import Object
from explosion import Explosion
from bullet import Bullet
import utils

class Target(Object):

    @staticmethod
    def position_shift(obj, game):
        new_pos = [obj.pos[idx] + obj.speed[idx] for idx, ignored in enumerate(obj.pos)]
        to_hit_units = [o for o in game.units
                        if o.active and o != obj and utils.dist(o.pos, new_pos) < (o.radius + obj.radius)]
        for to_hit in to_hit_units:
            to_hit.speed, obj.speed = obj.speed, to_hit.speed
            break
        else:
            obj.pos = new_pos

    def __init__(self, pos, speed, radius):
        super().__init__(pos, speed, radius)
        self.on_get_hit = []

        def damage(obj, game):
            obj.hp -= 1
            if obj.hp <= 0:
                obj.active = False
                game.effects.append(Explosion(obj))
        self.hp = 1
        if random() < 0.5: self.hp += 1
        if random() < 0.5: self.hp += 1
        self.on_get_hit.append(damage)

        @utils.with_chance(0.001)
        def spawn(obj, game):
            game.effects.append(Bullet(
                self.pos,
                [(random()-0.5)*2., 1. + random()*1.],
                5.
            ))
        self.on_update.append(spawn)

    def draw(self, surface):
        if not self.active:
            return
        draw_pos = (int(self.pos[0]), int(self.pos[1]))
        pygame.draw.circle(surface, (255, 255, 255), draw_pos, int(self.radius), 0)
        for i in range(self.hp):
            pygame.draw.circle(surface, (0, 0, 0), draw_pos, int(self.radius) - 2*i, 1)

