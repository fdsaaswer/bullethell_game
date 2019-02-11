import pygame

class Object:

    @staticmethod
    def position_shift(obj, game):
        obj.pos = [obj.pos[idx] + obj.speed[idx] for idx, _ in enumerate(obj.pos)]

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