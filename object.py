import math
import utils


class Object:

    @staticmethod
    def position_shift(obj, game):
        max_speed = 5.
        if utils.norm(obj.speed) > max_speed:
            obj.speed = utils.normalize(obj.speed, max_speed)
        if obj.target_move:
            vector = [obj.target_move[0] - obj.pos[0],
                      obj.target_move[1] - obj.pos[1]]
            angle_target = utils.cartesian2polar(vector)[1]
            if utils.dist(obj.pos, obj.target_move) < obj.rotation_radius:
                angle_target += 0.5*math.pi + math.pi / 60.
                angle_max_shift = 2.*math.pi
            elif utils.dist(obj.pos, obj.target_move) > obj.rotation_radius > 0:
                angle_target += 0.5 * math.pi - math.pi / 60.
                angle_max_shift = 2.*math.pi
            else:
                angle_max_shift = math.pi / 60.
            obj_speed_polar = utils.cartesian2polar(obj.speed)
            obj_speed_polar[1] = utils.periodic_shift_to(obj_speed_polar[1], angle_target, angle_max_shift)
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
        self.target_move = None
        self.rotation_radius = 0.
        self.radius = radius
        self.is_active = True
        self.charge = 0.
        self.charge_speed = 0.
        self.on_update = [self.position_shift,
                          self.charge_up]
