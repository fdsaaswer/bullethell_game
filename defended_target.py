import math
from random import choice

import utils
from bullet import Bullet
from target import Target


class DefendedTarget(Target):

    DEFENDER_MAX_DISTANCE = 150.

    @staticmethod
    def take_damage(obj, game, source):
        if not obj.defenders:
            super(DefendedTarget, DefendedTarget).take_damage(obj, game, source)

    @staticmethod
    @utils.with_chance(0.001)
    def spawn(obj, game):
        vector = [game.player_pos[0] - obj.pos[0],
                  game.player_pos[1] - obj.pos[1]]
        angle = utils.cartesian2polar(vector)[1]
        for i in range(5):
            game.add_effect(Bullet(
                obj.pos.copy(),
                utils.polar2cartesian([3., angle + (math.pi/30.)*(i - 2)]),
                None, 1.
             ))

    def __init__(self, pos, speed):
        super().__init__(pos, speed, 25.)

        @utils.with_chance(0.01)
        def add_defender(obj, game):
            target_units = game.get_units(obj, self.DEFENDER_MAX_DISTANCE, lambda _, x: isinstance(x, Target))
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
        N = 50
        for o in self.defenders:
            for i in range(N):
                pos = [self.pos[0] + (o.pos[0] - self.pos[0]) * i / N,
                       self.pos[1] + (o.pos[1] - self.pos[1]) * i / N]
                if utils.dist(pos, o.pos) < o.radius:
                    continue
                if utils.dist(pos, self.pos) < self.radius:
                    continue
                pos = [int(pos[0]), int(pos[1])]
                surface.set_at(pos, (200., 200., 200.))

