import pygame
import pygame.locals
from random import random

from unit import Unit
from target import Target
from defended_target import DefendedTarget
from destroyer_target import DestroyerTarget
from player import Player
from player import Action
from background import Background
import utils


class Game:
    def __init__(self, width, height):
        pygame.init()
        self._surface = pygame.display.set_mode((width, height))
        self._bgr = Background(width, height)
        self._player = Player([width/2., height - 100.], [0., 0.])
        self._effects = []  # e.g. bullets, explosions, power-ups, etc
        self._units = [self._player]  # 'physical' objects, e.g. can collide
        self._width = width
        self._height = height

    def get_player(self):
        return self._player

    def add_unit(self, obj):
        self._units.append(obj)

    def add_effect(self, obj):
        self._effects.append(obj)

    def update_obj_pos(self, obj):
        obj.pos[0] += obj.speed[0]
        obj.pos[1] += obj.speed[1]

        if obj.pos[1] + obj.radius < 0.:
            obj.active = False

        if isinstance(obj, Player) and obj.pos[1] + obj.radius > self._height:
            utils.collide(obj, [obj.pos[0], self._height])
        if obj.pos[1] - obj.radius > self._height:
            obj.active = False

        if isinstance(obj, Unit) and obj.pos[0] - obj.radius < 0.:
            utils.collide(obj, [0., obj.pos[1]])
        if obj.pos[0] + obj.radius < 0.:
            obj.active = False

        if isinstance(obj, Unit) and obj.pos[0] + obj.radius > self._width:
            utils.collide(obj, [self._width, obj.pos[1]])
        if obj.pos[0] - obj.radius > self._width:
            obj.active = False

    def get_units(self, obj, radius, function): # get units in radius matching condition
        if radius == 0.:
            return [o for o in self._units if o.active and o != obj and function(obj, o)]
        else:
            return [o for o in self._units if o.active and utils.dist(o.pos, obj.pos) < radius and o != obj and function(obj, o)]

    def get_colliding_units(self, obj):
        return self.get_units(obj, 0., lambda obj, o: utils.dist(obj.pos, o.pos) < obj.radius + o.radius)

    def update(self):
        self._bgr.update()
        for objects in [self._effects, self._units]:
            print(len(objects))
            for i in range(len(objects) - 1, -1, -1):
                obj = objects[i]
                if obj.active:
                    for func in obj.on_update:
                        func(obj, self)
                if not obj.active:  # can be updated during function execution
                    del objects[i] # TODO: improve complexity
        if not self._player.active:
            exit(0)

        # Not essential:
        def _spawn(game, obj, chance):
            if random() >= chance:
                return
            if not game.get_colliding_units(obj):
                game.add_unit(obj)
        _spawn(self, Target(
                [random() * self._width, 0.],
                [(random() - 0.5) * 2., random() * 1.]
            ), 0.02)
        _spawn(self, DefendedTarget(
                [random() * self._width, 0.],
                [(random() - 0.5) * 2., random() * 1.]
            ), 0.001)
        _spawn(self, DestroyerTarget(
                [random() * self._width, 0.],
                [(random() - 0.5) * 2., random() * 1.]
            ), 0.001)

    def draw(self):
        self._bgr.draw(self._surface)
        for obj in self._units + self._effects:
            if obj.active:
                obj.draw(self, self._surface)
        pygame.display.flip()

    def process_event(self, event):
        key2action = {  # update in options
            pygame.K_SPACE: Action.ATTACK,
            pygame.K_LEFT: Action.MOVE_LEFT,
            pygame.K_RIGHT: Action.MOVE_RIGHT,
            pygame.K_UP: Action.MOVE_UP,
            pygame.K_DOWN: Action.MOVE_DOWN,
            pygame.K_LSHIFT: Action.SHIFT
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

