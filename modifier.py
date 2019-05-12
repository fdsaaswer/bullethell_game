import copy
from random import random
import math

from hit import Bullet
from hit import Explosion
import utils

import pygame
from random import choice

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


class SpreadShot(BaseModifier):

    def __init__(self, holder, duration, count=4, spread=5.*random() + 10.):
        super().__init__(holder, duration)
        if count <= 1:
            raise AttributeError("Can not spread into less than 2 bullets")
        self._count = count
        self._spread = spread * math.pi / 180.

        def spread_shot(obj, game, bullet):
            ro, phi = utils.cartesian2polar(bullet.speed)
            for i in range(self._count):
                angle = phi - self._spread + 2. * self._spread * i / (self._count - 1.)
                bullet_new = copy.copy(bullet)
                bullet_new.pos = bullet.pos.copy()
                bullet_new.speed = utils.polar2cartesian([ro, angle])
                game.add_effect(bullet_new)
            bullet.is_active = False

        self._effect = spread_shot
        self._holder.on_shoot.append(self._effect)

    def detach(self):
        self._holder.on_shoot.remove(self._effect)

    def draw(self, game, surface, erase):
        if erase:
            color = (255., 255., 255.)
        else:
            color = (50., 50., 200.) if self._holder == game.get_player() else (200., 50., 50.)
        for i in range(self._count):
            phi = utils.cartesian2polar([
                    self._holder.target_shoot[0] - self._holder.pos[0],
                    self._holder.target_shoot[1] - self._holder.pos[1]
                  ])[1] if self._holder.target_shoot else -0.5*math.pi
            vector = utils.polar2cartesian([1., phi - self._spread + 2. * self._spread * i / (self._count - 1.)])
            N = 10
            for idx in range(N//2, N + N//2):
                draw_pos = [
                    int(self._holder.pos[0] + 2. * self._holder.radius * vector[0] * idx / N),
                    int(self._holder.pos[1] + 2. * self._holder.radius * vector[1] * idx / N),
                ]
                surface.set_at(draw_pos, color)


class ActiveDefense(BaseModifier):

    @staticmethod
    def spawn_bullet(self, game):
        if self._spawn_countdown == 0:
            self._spawn_countdown = self._spawn_period
            self._bullets = [o for o in self._bullets if o.is_active]
            if len(self._bullets) == self._max_bullets:
                return
            shift = utils.polar2cartesian([self._rotation_radius, 2. * math.pi * self._spawn_countdown / self._spawn_period])
            spawn_pos = [self._holder.pos[0] + shift[0], self._holder.pos[1] + shift[1]]
            bullet = Bullet(spawn_pos, [0., 3.], self._holder, self._damage)
            bullet.target_move = self._holder.pos
            bullet.rotation_radius = self._rotation_radius
            game.add_effect(bullet)
            self._bullets.append(bullet)
            self._game.append(game)
        self._spawn_countdown -= 1

    def __init__(self, holder, duration, rotation_radius=100.*random()+50., damage=0.5):
        super().__init__(holder, duration)
        self._bullets = []
        self._game = []
        self._max_bullets = 5
        self._spawn_period = 100
        self._spawn_countdown = 0
        self._rotation_radius = rotation_radius
        self._damage = damage
        self.on_update.append(self.spawn_bullet)

    def detach(self):
        for bullet, game in zip(self._bullets, self._game):
            explosion = Explosion(bullet.pos.copy(), self._holder, self._damage)
            game.add_effect(explosion)
            bullet.is_active = False

    def draw(self, game, surface, erase):
        if erase:
            color = (255., 255., 255.,)
        else:
            color = (0., 0., 255.) if self._holder == game.get_player() else (255., 0., 0.)
        shift = utils.polar2cartesian([self._rotation_radius, 2.*math.pi*self._spawn_countdown/self._spawn_period])
        draw_pos = [round(self._holder.pos[0] + shift[0]),
                    round(self._holder.pos[1] + shift[1])]
        pygame.draw.circle(surface, color, draw_pos, 3, 1)


class DelayedShot(BaseModifier):

    def __init__(self, holder, duration, game, damage, speed):
        super().__init__(holder, duration)
        self._game = game
        self._bullet_damage = damage
        self._bullet_speed = speed

    def detach(self):
        self._holder.shoot(self._holder, self._game, 0., self._bullet_speed, self._bullet_damage)

    def draw(self, game, surface, erase):
        pass


class ChainShot(BaseModifier):

    def __init__(self, holder, duration, damage_drop=0.3):
        super().__init__(holder, duration)
        self._gfx_radii = []
        self._gfx_phi = []
        self._damage_drop = damage_drop

        def start_auto_shot(obj, game, bullet):
            if bullet.damage > 0.1:
                game.add_effect(DelayedShot(obj, 10., game, bullet.damage * self._damage_drop, bullet.speed))
        self._effect = start_auto_shot
        self._holder.on_shoot.append(self._effect)

    def detach(self):
        self._holder.on_shoot.remove(self._effect)

    def draw(self, game, surface, erase):
        N = 50
        if erase:
            color = (255., 255., 255.)
        else:
            color = (0., 0., 255.) if self._holder == game.get_player() else (255., 0., 0.)
            self._gfx_phi.clear()
            self._gfx_radii.clear()
            for i in range(N):
                self._gfx_phi.append(random() * 2 * math.pi)
                self._gfx_radii.append(self._holder.radius + 6. + random() * 6.0)
        for i in range(N):
            vector_start = utils.polar2cartesian([self._gfx_radii[i], self._gfx_phi[i]])
            vector_end = utils.polar2cartesian([self._holder.radius + 5., self._gfx_phi[i]])
            pos_start = [round(self._holder.pos[0] + vector_start[0] - 1.),
                         round(self._holder.pos[1] + vector_start[1] - 1.)]
            pos_end = [round(self._holder.pos[0] + vector_end[0] - 1.),
                       round(self._holder.pos[1] + vector_end[1] - 1.)]
            pygame.draw.line(surface, color, pos_start, pos_end)


class SplashShot(BaseModifier):

    def __init__(self, holder, duration):
        super().__init__(holder, duration)

        def splash_attack(obj, game, target):
            explosion = Explosion(obj.pos.copy(), obj.source, obj.damage)
            game.add_effect(explosion)

        def add_splash_attack(obj, game, bullet):
            bullet.on_hit.append(splash_attack)

        self._effect = add_splash_attack
        self._holder.on_shoot.append(self._effect)

    def detach(self):
        self._holder.on_shoot.remove(self._effect)

    def draw(self, game, surface, erase):
        pass


class Defenders(BaseModifier):

    def __init__(self, holder, duration):
        super().__init__(holder, duration)
        self._max_range = 150.
        self._defender = None

        @utils.with_chance(0.02)
        def update_defenders(obj, game):
            if self._defender:
                if not self._defender.is_active or utils.dist(self._defender.pos, obj.pos) > 1.5 * self._max_range:
                    obj.defenders.remove(self._defender)
                    self._defender = None
            if not self._defender:
                targets = game.get_units(obj, self._max_range, lambda _, x: x not in obj.defenders)
                if targets:
                    self._defender = choice(targets)
                    obj.defenders.append(self._defender)

        self._effect = update_defenders
        self._holder.on_update.append(self._effect)

    def detach(self):
        self._holder.defenders = []
        self._holder.on_update.remove(self._effect)

    def draw(self, game, surface, erase):
        if not self._defender:
            return
        color = (255., 255., 255.) if erase else (200., 200., 200.)
        N = 50
        o = self._defender
        for i in range(N):
            pos = [self._holder.pos[0] + (o.pos[0] - self._holder.pos[0]) * (i*i) / (N*N),
                    self._holder.pos[1] + (o.pos[1] - self._holder.pos[1]) * (i*i) / (N*N)]
            if utils.dist(pos, o.pos) < o.radius:
                continue
            if utils.dist(pos, self._holder.pos) < self._holder.radius:
                continue
            draw_pos = [int(pos[0]), int(pos[1])]
            surface.set_at(draw_pos, color)

class ZapField(BaseModifier):

    @staticmethod
    def zap(obj, game):
        if obj._time_to_charge != 0:
            obj._time_to_charge -= 1
            return
        effects = game.get_effects(obj._holder, obj._max_range,
                                    lambda _, x: isinstance(x, Bullet) and obj._holder != x.source)
        if effects:
            bullet = choice(effects)
            bullet.is_active = False
            obj._time_to_charge = obj._recharge_period
            game.add_effect(Explosion(bullet.pos, obj._holder, bullet.damage))

    def __init__(self, holder, duration, range=75. + 25.*random()):
        super().__init__(holder, duration)
        self._max_range = range
        self._recharge_period = 100.
        self._time_to_charge = 0.
        self.on_update.append(self.zap)

    def detach(self):
        pass

    def draw(self, game, surface, erase):
        color = (255., 255., 255.) if erase else (200., 200., 200.)
        N = 72
        phi = 4 * math.pi * self._time_to_charge / self._recharge_period
        for i in range(N):
            if self._time_to_charge == 0:
                vector = utils.polar2cartesian([self._max_range, 2. * math.pi * i / N])
                pos = [self._holder.pos[0] + vector[0],
                       self._holder.pos[1] + vector[1]]
                draw_pos = [int(pos[0]), int(pos[1])]
                surface.set_at(draw_pos, color)
            else:
                vector = utils.polar2cartesian([
                    self._holder.radius + (self._max_range - self._holder.radius) * i / N,
                    phi + 2. * math.pi * i / N
                ])
                pos = [self._holder.pos[0] + vector[0],
                       self._holder.pos[1] + vector[1]]
                draw_pos = [int(pos[0]), int(pos[1])]
                surface.set_at(draw_pos, color)

