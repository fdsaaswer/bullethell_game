import pygame
from random import random

from object import Unit
from explosion import Explosion
from bullet import Bullet
import utils


class Target(Unit):

    def __init__(self, pos, speed, radius):
        super().__init__(pos, speed, radius)

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
                self.pos.copy(),
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

