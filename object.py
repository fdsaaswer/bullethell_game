import math
import utils


class Object:

    @staticmethod
    def position_shift(obj, game):
        max_speed = 10.
        speed_squared = obj.speed[0]**2 + obj.speed[1]**2
        if speed_squared > max_speed**2:
            obj.speed[0] *= max_speed / math.sqrt(speed_squared)
            obj.speed[1] *= max_speed / math.sqrt(speed_squared)
        if obj.target:
            vector = [obj.target.pos[0] - obj.pos[0],
                      obj.target.pos[1] - obj.pos[1]]
            angle_target = utils.cartesian2polar(vector)[1]
            if obj.anchor:
                angle_target += 0.5*math.pi
            obj_speed_polar = utils.cartesian2polar(obj.speed)
            obj_speed_polar[1] = utils.shift_to(obj_speed_polar[1], angle_target, 0.01)
            obj.speed = utils.polar2cartesian(obj_speed_polar)

        game.update_obj_pos(obj)

    @staticmethod
    def charge_up(obj, game):
        if obj.charge_speed:
            obj.charge = max(0., min(1., obj.charge + obj.charge_speed))

    def __init__(self, pos, speed, radius):
        if len(pos) != len(speed):
            raise AttributeError("Position and speed dimensions need to match")
        self.pos = pos
        self.speed = speed
        self.target = None
        self.anchor = False
        self.radius = radius
        self.active = True
        self.charge = 0.
        self.charge_speed = 0.
        self.on_update = []
        self.on_update.append(self.position_shift)
        self.on_update.append(self.charge_up)
