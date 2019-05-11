import utils

from random import random
from object import Object
from explosion import Explosion
from bullet import Bullet
from pickup import PickUp

import pygame
import math

class Unit(Object):


    @staticmethod
    def shoot(obj, game):
        if obj.charge < 0.1:
            return
        obj.charge -= 0.1
        if obj.target_shoot:
            vector = [obj.target_shoot[0] - obj.pos[0],
                      obj.target_shoot[1] - obj.pos[1]]
            speed = utils.normalize(vector, 1.5 + 0.5*random())
        else:
            speed = utils.normalize(obj.speed, 1.5 + 0.5*random())
        bullet = Bullet(obj.pos.copy(), speed, obj, obj.damage)
        game.add_effect(bullet)
        for func in obj.on_shoot:
            func(obj, game, bullet)

    @staticmethod
    def collision(obj, game):
        temp_colliding_units = game.get_colliding_units(obj)
        for to_hit in temp_colliding_units:
            if to_hit not in obj.colliding_units:
                to_hit.colliding_units.append(obj)
                utils.collide(to_hit, obj.pos)
                utils.collide(obj, to_hit.pos)
        obj.colliding_units = temp_colliding_units

    @staticmethod
    def take_damage(obj, game, source):
        if obj.defenders:
            return
        obj.hp -= source.damage
        if obj.hp < 1.:
            obj.is_active = False
            game.add_effect(Explosion(obj.pos.copy(), None, 1.0))
            if random() < 0.1 * obj.score_cost:
                pickup = PickUp(obj.pos.copy())
                pickup.target_move = game.get_player().pos
                game.add_effect(pickup)
            if source.source:
                for func in source.source.on_kill:
                    func(obj, game)

    def __init__(self, pos, speed, radius=15.):
        super().__init__(pos, speed, radius)
        self.defenders = []
        self.on_shoot = []
        self.on_hit = []
        self.on_get_hit = [self.take_damage]
        self.on_kill = []
        self.on_update = [self.position_shift,
                          self.collision,
                          self.charge_up,
                          self.shoot]
        self.target_shoot = None
        self.colliding_units = []
        self.hp = 1.
        self.damage = 0.5
        self.score_cost = 1.
        self.charge_speed = 0.001 * random()



    def draw(self, game, surface, erase):
        if erase:
            color_inner = (255., 255., 255.)
            color_outer = (255., 255., 255.)
            color_charged = (255., 255., 255.)
        else:
            color_inner = [255. - 155.*(self.hp % 1.)] * 3
            color_outer = (0., 0., 0.)
            color_intensity = 150.*self.charge if self.charge < 1. else 255.
            color_charged = (0., 0., color_intensity) if self == game.get_player() else (color_intensity, 0., 0.)
        draw_pos = (int(self.pos[0]), int(self.pos[1]))
        for i in range(int(self.hp)):
            if i == 0:
                pygame.draw.circle(surface, color_charged, draw_pos, int(self.radius), 1)
            elif self.radius > 2*i:
                pygame.draw.circle(surface, color_outer, draw_pos, int(self.radius) - 2*i, 1)
        if self.hp % 1 > 0.1 and self.radius > 2*(i+1):
            pygame.draw.circle(surface, color_inner, draw_pos, int(self.radius) - 2*(i+1), 1)

        if self.target_shoot:
            color = (255., 255., 255.,) if erase else (50., 50., 50.)
            vector = [self.target_shoot[0] - self.pos[0],
                      self.target_shoot[1] - self.pos[1]]
            phi = utils.cartesian2polar(vector)[1]
            points = []
            for vertex in [utils.polar2cartesian([self.radius + 3., phi - 0.05 * math.pi]),
                           utils.polar2cartesian([self.radius + 6., phi]),
                           utils.polar2cartesian([self.radius + 3., phi + 0.05 * math.pi])]:
                points.append([round(self.pos[0] + vertex[0]),
                               round(self.pos[1] + vertex[1])])
            pygame.draw.lines(surface, color, True, points, 1)
