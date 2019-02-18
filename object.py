class Object:

    @staticmethod
    def position_shift(obj, game):
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
