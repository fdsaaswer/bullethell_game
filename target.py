from random import random

import pygame

import utils
from bullet import Bullet
from unit import Unit

class Target(Unit):

    @staticmethod
    def shoot(obj, game):
        if obj.charge < 1.:
            return
        obj.charge = 0.
        if obj.target_shoot:
            vector = [obj.target_shoot[0] - obj.pos[0],
                      obj.target_shoot[1] - obj.pos[1]]
            speed = utils.normalize(vector, 1.5 + 0.5*random())
        else:
            speed = [2.*(random() - 0.5), 1. + 1.*random()]
        bullet = Bullet(obj.pos.copy(), speed, None, 1.)
        game.add_effect(bullet)
        for func in obj.on_shoot:
            func(obj, game, bullet)

    def __init__(self, pos, speed, radius=15.):
        super().__init__(pos, speed, radius)
        if random() < 0.5: self.hp += 1.
        if random() < 0.5: self.hp += 1.
        self.on_update.append(self.shoot)
        self.charge_speed = 0.005 * random()

    def draw(self, game, surface):
        super().draw(game, surface)
        draw_pos = (int(self.pos[0]), int(self.pos[1]))
        pygame.draw.circle(surface, [255] * 3, draw_pos, int(self.radius), 0)
        for i in range(int(self.hp)):
            pygame.draw.circle(surface, [0] * 3, draw_pos, int(self.radius) - 2*i, 1)
        if self.hp % 1 > 0.1:
            pygame.draw.circle(surface, [255. - 155.*(self.hp % 1.)] * 3, draw_pos, int(self.radius) - 2*(i+1), 1)
