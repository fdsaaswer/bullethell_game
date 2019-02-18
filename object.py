import math

class Object:

    @staticmethod
    def position_shift(obj, game):
        max_speed = 10.
        speed_squared = obj.speed[0]**2 + obj.speed[1]**2
        if speed_squared > max_speed**2:
            obj.speed[0] *= max_speed / math.sqrt(speed_squared)
            obj.speed[1] *= max_speed / math.sqrt(speed_squared)
        game.update_obj_pos(obj)

    @staticmethod
    def charge_up(obj, game):
        if obj.charge < 1. and obj.charge_speed > 0.:
            obj.charge += obj.charge_speed

    def __init__(self, pos, speed, radius):
        if len(pos) != len(speed):
            raise AttributeError("Position and speed dimensions need to match")
        self.pos = pos
        self.speed = speed
        self.radius = radius
        self.active = True
        self.charge = 0.
        self.charge_speed = 0.
        self.on_update = []
        self.on_update.append(self.position_shift)
        self.on_update.append(self.charge_up)
