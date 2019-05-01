import utils

from random import random
from object import Object
from explosion import Explosion
from pickup import PickUp

import pygame
import math

class Unit(Object):

    @staticmethod
    def position_shift(obj, game):
        super(Unit, Unit).position_shift(obj, game)
        temp_colliding_units = game.get_colliding_units(obj)
        for to_hit in temp_colliding_units:
            if to_hit not in obj.colliding_units:
                to_hit.colliding_units.append(obj)
                utils.collide(to_hit, obj.pos)
                utils.collide(obj, to_hit.pos)
        obj.colliding_units = temp_colliding_units

    @staticmethod
    def take_damage(obj, game, source):
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

    def __init__(self, pos, speed, radius):
        super().__init__(pos, speed, radius)
        self.target_shoot = None
        self.on_shoot = []
        self.on_hit = []
        self.on_get_hit = [self.take_damage]
        self.on_kill = []
        self.colliding_units = []
        self.hp = 1.
        self.score_cost = 1.

    def draw(self, game, surface):
        if self.target_shoot:
            color = (50., 50., 50)
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
