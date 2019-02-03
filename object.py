import pygame

class Object:

    @staticmethod
    def position_shift(obj, game):
        obj.pos = [obj.pos[idx] + obj.speed[idx] for idx, ignored in enumerate(obj.pos)]

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

class Explosion(Object):
    def __init__(self, obj):
        super().__init__(obj.pos, [0., 1.], 10)

        def charge_up(obj, game):
            if obj.charge < 1.5:
                obj.charge += 0.01
            else:
                obj.active = False
        self.charge = 0
        self.on_update = [charge_up]

    def draw(self, surface):
        if not self.active:
            return
        color = (255. - self.charge*200. if self.charge < 1. else 0., 0., 0.)
        draw_pos = (int(self.pos[0]), int(self.pos[1]))
        pygame.draw.circle(surface, color, draw_pos, int(max(1, float(self.radius)*5.*self.charge)), 1)