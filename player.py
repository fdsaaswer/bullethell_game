import pygame
import math
from enum import IntEnum

from object import Unit
from bullet import Bullet


class Action(IntEnum):
    NO_ACTION = 0
    MOVE_LEFT = 1
    MOVE_RIGHT = 2
    MOVE_UP = 4
    MOVE_DOWN = 8
    ATTACK = 16

class Player(Unit):

    def __init__(self, pos, speed):
        super().__init__(pos, speed, 15.)
        self.score = 0

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
                        [0., -1.]
                    )
                    game.effects.append(bullet)

                    def player_score(obj, game):
                        self.score += 1
                    bullet.on_hit.append(player_score)
        self.on_update.append(process_action)
        self.action = Action.NO_ACTION

        def charge_up(obj, game):
            if obj.charge < 1.:
                obj.charge += 0.001
        self.charge = 0.
        self.on_update.append(charge_up)

        def game_over(obj, game):
            exit(0)
        self.on_get_hit.append(game_over)

    def draw(self, surface):
        if not self.active:
            return
        draw_pos = (int(self.pos[0]), int(self.pos[1]))
        pygame.draw.circle(surface, (0, 0, 0), draw_pos, int(self.radius), 0)
        pygame.draw.circle(surface,
                           (self.charge*150. if self.charge < 1. else 255., 0, 0),
                           draw_pos, int(self.radius), 4)
        pygame.font.init()
        font = pygame.font.SysFont('consolas', 20)
        text_surface = font.render(str(self.score), True, (255, 0, 0))
        surface.blit(text_surface, (50, 50, 100, 50))
