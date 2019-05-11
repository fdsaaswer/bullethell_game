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
        self._gfx_radii = []

    def draw(self, game, surface, erase):
        N = 3
        if erase:
            color = (255., 255., 255.)
        else:
            color = (0., 0., 255.)
            self._gfx_radii = [
                5. + random() * (self.radius - 5.),
                5. + random() * (self.radius - 5.),
                5. + random() * (self.radius - 5.)
            ]
        draw_pos = (round(self.pos[0]), round(self.pos[1]))
        pygame.draw.circle(surface, color, draw_pos, int(self.radius), 1)
        for radius in self._gfx_radii:
            pygame.draw.circle(surface, color, draw_pos, int(radius), 1)
