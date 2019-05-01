import pygame

from random import random
from object import Object
import utils


class PickUp(Object):

    @staticmethod
    def position_shift(obj, game): # consider moving this logic to Player class
        super(PickUp, PickUp).position_shift(obj, game)
        player = game.get_player()
        if utils.dist(player.pos, obj.pos) < obj.radius:
            game.player_powerup()
            player.hp += obj.healing
            obj.is_active = False

    def __init__(self, pos):
        self.healing = int(30.*random()) / 10.
        super().__init__(pos, [0., 2.], 12. + self.healing)

    def draw(self, game, surface):
        draw_pos = (round(self.pos[0]), round(self.pos[1]))
        pygame.draw.circle(surface, (0., 0., 255.), draw_pos, int(self.radius), 1)
        for i in range(3):
            pygame.draw.circle(surface, (0., 0., 255.), draw_pos, int(5. + random()*(self.radius - 5.)), 1)
