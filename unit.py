import utils

from object import Object
from explosion import Explosion


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
            if source.source:
                for func in source.source.on_kill:
                    func(obj, game)

    def __init__(self, pos, speed, radius):
        super().__init__(pos, speed, radius)
        self.on_hit = []
        self.on_get_hit = [self.take_damage]
        self.on_kill = []
        self.colliding_units = []
        self.hp = 1.
        self.score_cost = 1.
