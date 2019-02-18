import pygame
import pygame.locals
from random import random

from target import Target
from defended_target import DefendedTarget
from player import Player
from player import Action
from background import Background
import utils


class Game:
    def __init__(self, width, height):
        pygame.init()
        self._surface = pygame.display.set_mode((width, height))
        self._bgr = Background(width, height)
        self._player = Player(
            [width/2., height - 100.],
            [0., 0.]
        )
        self.effects = []  # e.g. bullets, explosions, power-ups, etc
        self.units = [self._player]  # 'physical' objects, e.g. can collide
        self.width = width
        self.height = height

    def _spawn(self, obj, chance):
        if random() >= chance:
            return
        if not utils.colliding_objects(obj, self):
            self.units.append(obj)

    @property
    def player_pos(self):
        return self._player.pos

    def update(self):
        self._bgr.update()
        for objects in [self.effects, self.units]:
            print(len(objects))
            for i in range(len(objects) - 1, -1, -1):
                obj = objects[i]
                if obj.active:
                    for func in obj.on_update:
                        func(obj, self)
                if not obj.active:  # can be updated during function execution
                    del objects[i]

        # Not essential:
        self._spawn(Target(
                [random() * self.width, 0.],
                [(random() - 0.5) * 2., random() * 1.]
            ), 0.02)
        self._spawn(DefendedTarget(
                [random() * self.width, 0.],
                [(random() - 0.5) * 2., random() * 1.]
            ), 0.002)

    def draw(self):
        self._bgr.draw(self._surface)
        for obj in self.units + self.effects:
            obj.draw(self._surface)
        pygame.display.flip()

    def process_event(self, event):
        key2action = {  # update in options
            pygame.K_SPACE: Action.ATTACK,
            pygame.K_LEFT: Action.MOVE_LEFT,
            pygame.K_RIGHT: Action.MOVE_RIGHT,
            pygame.K_UP: Action.MOVE_UP,
            pygame.K_DOWN: Action.MOVE_DOWN
        }

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit(0)
            try:
                self._player.action |= key2action[event.key]
            except KeyError:
                pass
        if event.type == pygame.KEYUP:
            try:
                self._player.action &= ~key2action[event.key]
            except KeyError:
                pass

