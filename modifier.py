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
        self._obj = None
        self._game = None

    def apply(self, obj, game):
        self._obj = obj
        self._game = game

    def detach(self):
        pass

    def update(self):
        if self._is_permanent:
            pass
        self._duration -= 1
        if self._duration == 0:
            self.is_active = False
        if not self.is_active:
            self.detach()

    def draw(self, obj, surface):
        pass


class TripleAttack(BaseModifier):

    def __init__(self):
        super().__init__(1000)
        self._spread = 0.2 * random()

        def triple_attack(obj, game, bullet):
            for speed_change in [-0.2 - self._spread, 0.2 + self._spread]:
                bullet_new = copy.copy(bullet)
                bullet_new.pos = bullet.pos.copy()
                bullet_new.speed = bullet.speed.copy()
                bullet_new.speed[0] += speed_change
                game.add_effect(bullet_new)
        self._effect = triple_attack

    def apply(self, obj, game):
        super().apply(obj, game)
        self._obj.on_shoot.append(self._effect)

    def detach(self):
        super().detach()
        self._obj.on_shoot.remove(self._effect)


class ActiveDefense(BaseModifier):
    def __init__(self):
        super().__init__(1500)
        self._bullets = []
        self._max_bullets = 5
        self._spawn_period = 100

    def update(self):
        super().update()
        self._bullets = [o for o in self._bullets if o.active]
        if self._duration % self._spawn_period == 0 and len(self._bullets) < self._max_bullets:
            bullet = Bullet(self._obj.pos.copy(), [0., 3.], self._obj, 1.5)
            bullet.target = self._obj
            bullet.anchor_radius = 100.*random() + 100.
            self._game.add_effect(bullet)
            self._bullets.append(bullet)

    def detach(self):
        for bullet in self._bullets:
            explosion = Explosion(bullet.pos.copy(), self._obj, 0.5)
            self._game.add_effect(explosion)
            bullet.active = False


class SplashAttack(BaseModifier):

    def __init__(self):
        super().__init__(1000)

        def splash_attack(obj, game, target):
            explosion = Explosion(target.pos.copy(), obj, 0.3)
            explosion.already_hit.add(target)
            explosion.radius += 5.
            game.add_effect(explosion)
        self._effect = splash_attack

    def apply(self, obj, game):
        super().apply(obj, game)
        self._obj.on_hit.append(self._effect)

    def detach(self):
        super().detach()
        self._obj.on_hit.remove(self._effect)


PLAYER_MODIFIERS = [TripleAttack, ActiveDefense, SplashAttack]