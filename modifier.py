import copy
from random import random
import math

from bullet import Bullet
from explosion import Explosion
import utils


class BaseModifier:
    def __init__(self, duration):
        self.is_active = True
        if duration:
            self._duration = duration
            self._is_permanent = False
        else:
            self._is_permanent = True

    def update(self, obj, game):
        if self._is_permanent:
            pass
        self._duration -= 1
        if self._duration == 0:
            self.is_active = False

    def apply(self, obj, game):
        pass

    def detach(self, obj, game):
        pass

    def draw(self, obj, surface):
        pass


class TripleAttack(BaseModifier):

    @staticmethod
    def triple_attack(obj, game, bullet):
        spread = 0.2 * random()
        for speed_change in [-0.2 - spread, 0.2 + spread]:
            bullet_new = copy.deepcopy(bullet)
            bullet_new.speed[0] += speed_change
            game.add_effect(bullet_new)

    def __init__(self):
        super().__init__(1000)
        self.effect = self.triple_attack

    def apply(self, obj, game):
        obj.on_shoot.append(self.effect)

    def detach(self, obj, game):
        obj.on_shoot.remove(self.effect)


class ActiveDefense(BaseModifier):
    def __init__(self):
        super().__init__(500)
        self.bullets = []

    def apply(self, obj, game):
        for i in range(6):
            vector = utils.polar2cartesian([35., 2.*math.pi*i/6.])
            speed = utils.polar2cartesian([3.5, 2.*math.pi*i/6.])
            bullet = Bullet([obj.pos[0] + vector[0], obj.pos[1] + vector[1]],
                            speed, obj, 1.5)
            bullet.target = obj
            bullet.anchor = True
            game.add_effect(bullet)
            self.bullets.append(bullet)

    def detach(self, obj, game):
        for bullet in self.bullets:
            if not bullet.active:
                continue
            explosion = Explosion(bullet.pos.copy(), obj, 1.5)
            game.add_effect(explosion)
            bullet.active = False


class SplashAttack(BaseModifier):

    @staticmethod
    def splash_attack(obj, game, target):
        explosion = Explosion(target.pos.copy(), obj, 0.3)
        explosion.already_hit.add(target)
        explosion.radius += 5.
        game.add_effect(explosion)

    def __init__(self):
        super().__init__(1000)
        self.effect = self.splash_attack

    def apply(self, obj, game):
        obj.on_hit.append(self.effect)

    def detach(self, obj, game):
        obj.on_hit.remove(self.effect)


PLAYER_MODIFIERS = [TripleAttack, ActiveDefense, SplashAttack]