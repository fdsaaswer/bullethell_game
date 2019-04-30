import copy
from random import random
import math

from bullet import Bullet
from explosion import Explosion
import utils


class BaseModifier:

    @staticmethod
    def process(self, game):
        if not self._holder.is_active:
            self.is_active = False
        if not self._is_permanent:
            self._duration -= 1
            if self._duration == 0:
                self.is_active = False
        if not self.is_active:
            self.detach()

    def __init__(self, holder, duration):
        self._holder = holder
        self.is_active = True
        if duration:
            self._duration = duration
            self._is_permanent = False
        else:
            self._is_permanent = True
        self.on_update = [self.process]

    def detach(self):
        pass

    def draw(self, game, surface):
        pass


class TripleAttack(BaseModifier):

    def __init__(self, holder):
        super().__init__(holder, 1000)
        self._spread = 0.2 * random()

        def triple_attack(obj, game, bullet):
            for speed_change in [-0.2 - self._spread, 0.2 + self._spread]:
                bullet_new = copy.copy(bullet)
                bullet_new.pos = bullet.pos.copy()
                bullet_new.speed = bullet.speed.copy()
                bullet_new.speed[0] += speed_change
                game.add_effect(bullet_new)
        self._effect = triple_attack
        self._holder.on_shoot.append(self._effect)

    def detach(self):
        self._holder.on_shoot.remove(self._effect)


class ActiveDefense(BaseModifier):

    @staticmethod
    def spawn_bullet(self, game):
        if self._spawn_countdown == 0:
            self._spawn_countdown = self._spawn_period
            self._bullets = [o for o in self._bullets if o.is_active]
            if len(self._bullets) == self._max_bullets:
                return
            bullet = Bullet(self._holder.pos.copy(), [0., 3.], self._holder, 1.5)
            bullet.target = self._holder
            bullet.anchor_radius = 100. * random() + 100.
            game.add_effect(bullet)
            self._bullets.append(bullet)
            self._game.append(game)
        self._spawn_countdown -= 1

    def __init__(self, holder):
        super().__init__(holder, 1500)
        self._bullets = []
        self._game = []
        self._max_bullets = 5
        self._spawn_period = 100
        self._spawn_countdown = 0
        self.on_update.append(self.spawn_bullet)

    def detach(self):
        for bullet, game in zip(self._bullets, self._game):
            explosion = Explosion(bullet.pos.copy(), self._holder, 0.5)
            game.add_effect(explosion)
            bullet.is_active = False
        super().detach()


class SplashAttack(BaseModifier):

    def __init__(self, holder):
        super().__init__(holder, 1000)

        def splash_attack(obj, game, target):
            explosion = Explosion(target.pos.copy(), obj, 0.3)
            explosion.already_hit.add(target)
            explosion.radius += 5.
            game.add_effect(explosion)
        self._effect = splash_attack
        self._holder.on_hit.append(self._effect)

    def detach(self):
        self._holder.on_hit.remove(self._effect)


class ShootAt(BaseModifier):

    def __init__(self, holder, target):
        super().__init__(holder, 0)
        self._target = target

        def shoot_at(obj, game, bullet):
            ro = utils.cartesian2polar(bullet.speed)[0]
            vector = [self._target.pos[0] - obj.pos[0],
                      self._target.pos[1] - obj.pos[1]]
            phi = utils.cartesian2polar(vector)[1]
            bullet.speed = utils.polar2cartesian([ro, phi])
        self._effect = shoot_at
        self._holder.on_shoot.append(self._effect)

    def detach(self):
        self._holder.on_shoot.remove(self._effect)

    def draw(self, game, surface):
        vector = utils.normalize([
            self._target.pos[0] - self._holder.pos[0],
            self._target.pos[1] - self._holder.pos[1]
        ])
        N = 10
        for i in range(3, N+3):
            draw_pos = [
                int(self._holder.pos[0] + 2. * self._holder.radius * vector[0] * i / N),
                int(self._holder.pos[1] + 2. * self._holder.radius * vector[1] * i / N),
            ]
            surface.set_at(draw_pos, (200., 50., 50.))


class SpreadShot(BaseModifier):

    def __init__(self, holder, count, spread):
        super().__init__(holder, 0)
        if count <= 1:
            raise AttributeError("Can not spread into less than 2 bullets")
        self._count = count
        self._spread = spread * math.pi / 180.

        def spread_shot(obj, game, bullet):
            ro, phi = utils.cartesian2polar(bullet.speed)
            for i in range(self._count):
                angle = phi - self._spread + 2.*self._spread*i/(self._count-1.)
                bullet_new = copy.copy(bullet)
                bullet_new.pos = bullet.pos.copy()
                bullet_new.speed = utils.polar2cartesian([ro, angle])
                game.add_effect(bullet_new)
            bullet.is_active = False
        self._effect = spread_shot
        self._holder.on_shoot.append(self._effect)

    def detach(self):
        self._holder.on_shoot.remove(self._effect)


PLAYER_MODIFIERS = [TripleAttack, ActiveDefense, SplashAttack]