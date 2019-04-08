import math
from random import choice

import utils
import modifier
from target import Target


class DefendedTarget(Target):

    DEFENDER_MAX_DISTANCE = 150.

    @staticmethod
    def take_damage(obj, game, source):
        if not obj.defenders:
            super(DefendedTarget, DefendedTarget).take_damage(obj, game, source)

    def __init__(self, pos, speed):
        super().__init__(pos, speed, 25.)
        self.score_cost = 10

        @utils.with_chance(0.01)
        def add_defender(obj, game):
            target_units = game.get_units(obj, self.DEFENDER_MAX_DISTANCE, lambda _, x: isinstance(x, Target))
            if target_units:
                obj.defenders.append(choice(target_units))

        def del_defender(obj, game):
            for i, o in enumerate(self.defenders):
                if not o.is_active or utils.dist(o.pos, obj.pos) > 2.*self.DEFENDER_MAX_DISTANCE:
                    del self.defenders[i]
        self.defenders = []
        self.on_update.extend([add_defender, del_defender])

    def draw(self, game, surface):
        super().draw(game, surface)
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

