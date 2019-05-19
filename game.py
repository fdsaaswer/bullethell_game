import pygame
import pygame.locals
from random import random

from unit import Unit
from player import Player
from player import Action
from background import Background
import utils
import modifier
from random import choice

class Game:
    def __init__(self, width, height):
        pygame.init()
        self._surface = pygame.display.set_mode((width, height))
        self._surface.fill((255., 255., 255.))
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

    def player_powerup(self):
        new_modifier = choice([
            modifier.HomingShot,
            modifier.ChainShot,
            modifier.SplashShot,
            modifier.SpreadShot,
            modifier.ActiveDefense,
            modifier.ZapField
        ])(self._player, 1000)
        self.add_effect(new_modifier)

    def add_effect(self, obj):
        self._effects.append(obj)

    def update_obj_pos(self, obj):
        obj.pos[0] += obj.speed[0]
        obj.pos[1] += obj.speed[1]

        if obj.pos[1] + obj.radius < 0.:
            obj.is_active = False

        if isinstance(obj, Player) and obj.pos[1] + obj.radius > self._height:
            utils.collide(obj, [obj.pos[0], self._height])
        if obj.pos[1] - obj.radius > self._height:
            obj.is_active = False

        if isinstance(obj, Unit) and obj.pos[0] - obj.radius < 0.:
            utils.collide(obj, [0., obj.pos[1]])
        if obj.pos[0] + obj.radius < 0.:
            obj.is_active = False

        if isinstance(obj, Unit) and obj.pos[0] + obj.radius > self._width:
            utils.collide(obj, [self._width, obj.pos[1]])
        if obj.pos[0] - obj.radius > self._width:
            obj.is_active = False

    def get_effects(self, obj, radius, function):
        if radius == 0.:
            return [o for o in self._effects if o.is_active and o != obj and function(obj, o)]
        else:
            return [o for o in self._effects if o.is_active and o != obj and function(obj, o) and utils.dist(o.pos, obj.pos) < radius ]

    def get_units(self, obj, radius, function): # get units in radius matching condition
        if radius == 0.:
            return [o for o in self._units if o.is_active and o != obj and function(obj, o)]
        else:
            return [o for o in self._units if o.is_active and o != obj and function(obj, o) and utils.dist(o.pos, obj.pos) < radius]

    def get_colliding_units(self, obj):
        return self.get_units(obj, 0., lambda o1, o2: utils.dist(o1.pos, o2.pos) < o1.radius + o2.radius)

    def update(self):
        self._bgr.update()
        for obj in self._units:
            if obj.is_active:
                for func in obj.on_update:
                    func(obj, self)
        self._units = [obj for obj in self._units if obj.is_active]

        for obj in self._effects:
            if obj.is_active:
                for func in obj.on_update:
                    func(obj, self)
        self._effects = [obj for obj in self._effects if obj.is_active]

        if not self._player.is_active:
            exit(0)
        if random() < 0.02:
            obj = Unit(
                [random() * self._width, 0.],
                [(random() - 0.5) * 2., random() * 1.]
            )
            if not self.get_colliding_units(obj):
                self.add_unit(obj)

            def apply_effect(game, obj, effect):
                obj.radius += 3.
                obj.hp += 1.0
                game.add_effect(effect)

            if random() < 0.3:
                obj.hp += 2.
            if random() < 0.3:
                obj.target_shoot = self.get_player().pos
                if random() < 0.05:
                    apply_effect(self, obj, modifier.ChainShot(obj, 0, 0.5))
                if random() < 0.05:
                    apply_effect(self, obj, modifier.SpreadShot(obj, 0, 5, 15.))
                if random() < 0.1:
                    apply_effect(self, obj, modifier.HomingShot(obj, 0, 0.5))
            if random() < 0.05:
                apply_effect(self, obj, modifier.Defenders(obj, 0))
            if random() < 0.05:
                apply_effect(self, obj, modifier.ActiveDefense(obj, 0, 50., 0.3))
                obj.target_move = self.get_player().pos
            if random() < 0.05:
                apply_effect(self, obj, modifier.ZapField(obj, 0, 50.))


    def draw(self, erase=False):
        #self._bgr.draw(self._surface)
        for obj in self._units + self._effects:
            if obj.is_active:
                obj.draw(self, self._surface, erase)
        if not erase:
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

