import pygame

from random import random
from object import Object
import utils

class PickUp(Object):

    @staticmethod
    def position_shift(obj, game):
        super(PickUp, PickUp).position_shift(obj, game)
        player = game.get_player()
        if utils.dist(player.pos, obj.pos) < obj.radius:
            player.hp += 3.
            player.score += 3.
            obj.active = False
        else:
            obj.speed[0] = 1. if obj.pos[0] < player.pos[0] else -1.

    def __init__(self, pos):
        super().__init__(pos, [0., 2.], 15.)

    def draw(self, surface):
        if not self.active:
            return
        draw_pos = (round(self.pos[0]), round(self.pos[1]))
        pygame.draw.circle(surface, (0., 0., 255.), draw_pos, int(self.radius), 1)
        for i in range(3):
            pygame.draw.circle(surface, (0., 0., 255.), draw_pos, int(3. + random()*(self.radius - 3.)), 1)
