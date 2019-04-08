import utils

from random import random
from object import Object
from explosion import Explosion
from pickup import PickUp

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
            obj.active = False
            game.add_effect(Explosion(obj.pos.copy(), None, 1.0))
            if random() < 0.1 * obj.score_cost:
                pickup = PickUp(obj.pos.copy())
                pickup.target = game.get_player()
                game.add_effect(pickup)
            if source.source:
                for func in source.source.on_kill:
                    func(obj, game)

    @staticmethod
    def process_modifiers(obj, game):
        def process_modifier(o):
            o.update()
            return o
        obj.modifiers = [process_modifier(o) for o in obj.modifiers if o.is_active]

    def __init__(self, pos, speed, radius):
        super().__init__(pos, speed, radius)
        self.on_shoot = []
        self.modifiers = []
        self.on_update.append(self.process_modifiers)
        self.on_hit = []
        self.on_get_hit = [self.take_damage]
        self.on_kill = []
        self.colliding_units = []
        self.hp = 1.
        self.score_cost = 1.

    def draw(self, game, surface):
        for o in self.modifiers:
            o.draw(self, surface)
