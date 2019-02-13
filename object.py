import utils

class Object:

    @staticmethod
    def position_shift(obj, game):
        obj.pos[0] += obj.speed[0]
        obj.pos[1] += obj.speed[1]

    def __init__(self, pos, speed, radius):
        if len(pos) != len(speed):
            raise AttributeError("Position and speed dimensions need to match")
        self.pos = pos
        self.speed = speed
        self.radius = radius
        self.active = True
        self.on_update = []

        self.on_update.append(self.position_shift)

        def delete(obj, game):
            if self.pos[1] > game.height:
                obj.active = False
            if self.pos[0] + self.radius < 0:
                obj.active = False
            if self.pos[0] - self.radius > game.width:
                obj.active = False
        self.on_update.append(delete)

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

    def __init__(self, pos, speed, radius):
        super().__init__(pos, speed, radius)
        self.on_get_hit = []
        self.colliding_objects = []
