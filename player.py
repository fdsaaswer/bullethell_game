from enum import IntEnum

import pygame

from bullet import Bullet
from explosion import Explosion
from unit import Unit


class Action(IntEnum):
    NO_ACTION = 0
    MOVE_LEFT = 1
    MOVE_RIGHT = 2
    MOVE_UP = 4
    MOVE_DOWN = 8
    ATTACK = 16


class Player(Unit):

    @staticmethod
    def process_action(obj, game):
        if obj.action & Action.MOVE_LEFT and obj.action & Action.MOVE_RIGHT:
            pass
        elif obj.action & Action.MOVE_LEFT:
            obj.speed[0] -= 0.1
        elif obj.action & Action.MOVE_RIGHT:
            obj.speed[0] += 0.1
        if obj.action & Action.MOVE_UP and obj.action & Action.MOVE_DOWN:
            pass
        elif obj.action & Action.MOVE_UP:
            obj.speed[1] -= 0.05
        elif obj.action & Action.MOVE_DOWN:
            obj.speed[1] += 0.05
        if obj.action & Action.ATTACK:
            obj.action &= ~Action.ATTACK
            if obj.charge >= 0.1:
                obj.charge -= 0.1
                bullet = Bullet(
                    obj.pos.copy(),
                    [0., -3.],
                    obj, obj.damage
                )
                bullet.charge_speed *= 3
                game.add_effect(bullet)
                for func in obj.on_shoot:
                    func(obj, game, bullet)

    def __init__(self, pos, speed):
        super().__init__(pos, speed, 15.)

        def player_score(obj, game):
            self.score += obj.score_cost

        def player_damaged(obj, game, source):
            game.add_effect(Explosion(obj.pos.copy(), obj, source.damage))

        self.on_get_hit.append(player_damaged)
        self.on_kill.append(player_score)
        self.on_update = [self.position_shift,
                          self.collision,
                          self.charge_up,
                          self.process_action]
        self.action = Action.NO_ACTION
        self.hp += 3.
        self.damage = 0.4
        self.score = 0
        self.charge_speed = 0.001

