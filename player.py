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
    SHIFT = 32


def process_action(obj, game):
    obj.charge_speed = -0.002 if obj.action & Action.SHIFT else 0.001
    if obj.action & Action.MOVE_LEFT and obj.action & Action.MOVE_RIGHT:
        pass
    elif obj.action & Action.MOVE_LEFT:
        obj.speed[0] -= 0.5 if obj.action & Action.SHIFT and obj.charge > 0 else 0.1
    elif obj.action & Action.MOVE_RIGHT:
        obj.speed[0] += 0.5 if obj.action & Action.SHIFT and obj.charge > 0 else 0.1
    if obj.action & Action.MOVE_UP and obj.action & Action.MOVE_DOWN:
        pass
    elif obj.action & Action.MOVE_UP:
        obj.speed[1] -= 0.25 if obj.action & Action.SHIFT and obj.charge > 0 else 0.05
    elif obj.action & Action.MOVE_DOWN:
        obj.speed[1] += 0.25 if obj.action & Action.SHIFT and obj.charge > 0 else 0.05
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


class Player(Unit):

    def __init__(self, pos, speed):
        super().__init__(pos, speed, 15.)

        def player_score(obj, game):
            self.score += obj.score_cost

        def player_damaged(obj, game, source):
            game.add_effect(Explosion(obj.pos.copy(), obj, source.damage))

        self.on_get_hit.append(player_damaged)
        self.on_kill.append(player_score)
        self.on_update.append(process_action)
        self.action = Action.NO_ACTION
        self.hp += 3.
        self.damage = 0.4
        self.score = 0

    def draw(self, surface):
        if not self.active:
            return
        draw_pos = (int(self.pos[0]), int(self.pos[1]))
        pygame.draw.circle(surface, (0, 0, 0), draw_pos, int(self.radius), 0)
        pygame.draw.circle(surface,
                           (self.charge * 150. if self.charge < 1. else 255., 0, 0),
                           draw_pos, int(self.radius), 4)
        pygame.font.init()
        font = pygame.font.SysFont('consolas', 20)
        text_surface = font.render(str(self.score) + ', ' + str(self.hp), True, (255, 0, 0))
        surface.blit(text_surface, (50, 50, 100, 50))
