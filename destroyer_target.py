import pygame
import math
from random import gauss
from random import random

import utils
from bullet import Bullet
from explosion import Explosion
from target import Target


class DestroyerTarget(Target):

    @staticmethod
    def take_damage(obj, game):
        super(DestroyerTarget, DestroyerTarget).take_damage(obj, game)
        if obj.charge < 0.7:
            return
        for i in range(3):
            explosion = Explosion([obj.pos[0] + gauss(0., 20.),
                                   obj.pos[1] + gauss(0., 20.)])
            explosion.radius += random() * 3.0
            explosion.already_hit.add(obj)
            game.add_effect(explosion)

    @staticmethod
    @utils.with_chance(0.08)
    def spawn(obj, game):
        if obj.charge >= 1:
            obj.charge = 0.
        if obj.charge < 0.7:
            return
        vector = [game.player_pos[0] - obj.pos[0],
                  game.player_pos[1] - obj.pos[1]]
        angle = utils.cartesian2polar(vector)[1]
        bullet = Bullet(
            obj.pos.copy(),
            utils.polar2cartesian([3., angle + gauss(0., 1.) * math.pi / 30.])
        )
        game.add_effect(bullet)

    def __init__(self, pos, speed):
        super().__init__(pos, speed, 15.)
        self.charge_speed = 0.002


    def draw(self, surface):
        super().draw(surface)
        N = 50
        for i in range(N):
            phi = random() * 2 * math.pi
            vector1 = utils.polar2cartesian([self.radius + 1. + random() * 5.0, phi])
            pos1 = [int(vector1[0] + self.pos[0]),
                    int(vector1[1] + self.pos[1])]
            vector2 = utils.polar2cartesian([self.radius + 1., phi])
            pos2 = [int(vector2[0] + self.pos[0]),
                    int(vector2[1] + self.pos[1])]
            pygame.draw.line(surface, (0. if self.charge < 0.7 else 255., 0., 0.), pos1, pos2)


