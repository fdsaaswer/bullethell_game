import utils

from object import Object
from explosion import Explosion

class Unit(Object):

    @staticmethod
    def position_shift(obj, game):
        super(Unit, Unit).position_shift(obj, game)
        temp_colliding_objects = utils.colliding_objects(obj, game)
        for to_hit in temp_colliding_objects:
            if to_hit not in obj.colliding_objects:
                to_hit.colliding_objects.append(obj)
                utils.collide(to_hit, obj)
                utils.collide(obj, to_hit)
        obj.colliding_objects = temp_colliding_objects

    @staticmethod
    def take_damage(obj, game):
        obj.hp -= 1
        if obj.hp <= 0:
            obj.active = False
            game.effects.append(Explosion(obj))

    def __init__(self, pos, speed, radius):
        super().__init__(pos, speed, radius)
        self.on_get_hit = [self.take_damage]
        self.colliding_objects = []
