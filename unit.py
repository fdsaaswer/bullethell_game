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
    def take_damage(obj, game):
        obj.hp -= 1.
        if obj.hp < 1.:
            obj.active = False
            game.add_effect(Explosion(obj.pos.copy()))

    def __init__(self, pos, speed, radius):
        super().__init__(pos, speed, radius)
        self.on_get_hit = [self.take_damage]
        self.hp = 1.
        self.colliding_units = []
