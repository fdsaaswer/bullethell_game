class Object:

    @staticmethod
    def position_shift(obj, game):
        obj.pos[0] += obj.speed[0]
        obj.pos[1] += obj.speed[1]
        if obj.pos[1] + obj.radius < 0:
            obj.active = False
        if obj.pos[1] - obj.radius > game.height:
            obj.active = False
        if obj.pos[0] + obj.radius < 0:
            obj.active = False
        if obj.pos[0] - obj.radius > game.width:
            obj.active = False

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
