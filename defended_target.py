import pygame
import math
from random import choice

from target import Target
from bullet import Bullet
import utils


class DefendedTarget(Target):

    DEFENDER_MAX_DISTANCE = 150.

    @staticmethod
    def damage(obj, game):
        if obj.defenders:
            pass
        else:
            super(DefendedTarget, DefendedTarget).damage(obj, game)

    @staticmethod
    @utils.with_chance(0.001)
    def spawn(obj, game):
        vector = [game._player.pos[0] - obj.pos[0],
                  game._player.pos[1] - obj.pos[1]]
        angle = utils.cartesian2polar(vector)[1]
        for i in range(5):
            game.effects.append(Bullet(
                obj.pos.copy(),
                utils.polar2cartesian([3., angle + (math.pi/30.)*(i - 2)])
             ))

    def __init__(self, pos, speed):
        super().__init__(pos, speed, 25.)

        @utils.with_chance(0.01)
        def add_defender(obj, game):
            target_units = utils.units_in_radius_matching_condition(obj, game, self.DEFENDER_MAX_DISTANCE, lambda x: True)
            if target_units:
                obj.defenders.append(choice(target_units))

        def del_defender(obj, game):
            for i, o in enumerate(self.defenders):
                if not o.active or utils.dist(o.pos, obj.pos) > 2.*self.DEFENDER_MAX_DISTANCE:
                    del self.defenders[i]
        self.defenders = []
        self.on_update.extend([add_defender, del_defender])

    def draw(self, surface):
        super().draw(surface)
        for o in self.defenders:
            pygame.draw.line(surface, (200., 200., 200.), self.pos, o.pos)

