import pygame
import pygame.locals
import collections
import time
from random import random

from target import Target
import utils

class Background:

    def __init__(self, x, y, depth = 0):
        self.x = x
        self.y = y
        self.depth = depth
        self.color = random() * 100.
        self.children = []
        Node = collections.namedtuple("Node", "rect offset_x offset_y")
        if random() < 0.5 and depth < 6:
            offset = y*(random()*0.9 + 0.1)
            self.children.append(Node(rect=Background(x, offset, depth+1),
                                      offset_x=0, offset_y=0))
            self.children.append(Node(rect=Background(x, y-offset, depth+1),
                                      offset_x=0, offset_y=offset))
        elif random() < 0.5 and depth < 6:
            offset = x*(random()*0.9 + 0.1)
            self.children.append(Node(rect=Background(offset, y, depth+1),
                                      offset_x=0, offset_y=0))
            self.children.append(Node(rect=Background(x-offset, y, depth+1),
                                      offset_x=offset, offset_y=0))
        elif random() < 1. and x > 20 and y > 20:
            new_x_start = 10. + random()*90.
            new_x_end = x - (10. + random()*90.)
            new_y_start = 10. + random()*40.
            new_y_end = y - (10. + random()*40.)
            width = new_x_end - new_x_start
            height = new_y_end - new_y_start
            if width > 20. and height > 20.:
                self.rect = (new_x_start, new_y_start, width, height)
                if depth < 6:
                    self.children.append(Node(rect=Background(width, height, depth + 1),
                                              offset_x=new_x_start, offset_y=new_y_start))

    def draw(self, surface, offset_x, offset_y):
        #pygame.draw.rect(surface, (self.color, self.color, self.color), (offset_x, offset_y, self.x, self.y), 0)
        try:
            rect_to_draw = [self.rect[0] + offset_x,
                            self.rect[1] + offset_y,
                            self.rect[2],
                            self.rect[3]]
            pygame.draw.rect(surface, (0, 0, 0), rect_to_draw, 1)
        except AttributeError:
            pass
        for child in self.children:
            child.rect.draw(surface, child.offset_x + offset_x, child.offset_y + offset_y)


class Game:
    def __init__(self, width, height):
        self.bullets = []
        self.targets = []
        self.width = width
        self.height = height
        self.bgr = [Background(self.width, self.height),
                    Background(self.width, self.height)]
        self.bgr_active = 0
        self.bgr_offset = 0
        self.surface = pygame.display.set_mode((int(width), int(height)))
        pygame.init()

    def update(self):
        #spawn_target
        if random() < 0.1:
            spawn_pos = [random()*self.width, 0.]
            spawn_radius = 15
            for obj in self.targets:
                if utils.dist(spawn_pos, obj.pos) < (spawn_radius + obj.radius):
                    break
            else:
                self.targets.append(Target(
                    spawn_pos,
                    [(random()-0.5)*2., random()*1.],
                    spawn_radius
                ))
        for i in range(len(self.bullets) - 1, -1, -1):
            obj = self.bullets[i]
            for func in obj.on_update:
                func(obj, self)
            if not obj.active:
                del self.bullets[i]
        for i in range(len(self.targets) - 1, -1, -1):
            obj = self.targets[i]
            for func in obj.on_update:
                func(obj, self)
            if not obj.active:
                del self.targets[i]

    def draw(self):
        self.surface.fill((255, 255, 255))
        self.bgr[self.bgr_active].draw(self.surface, 0., self.bgr_offset - HEIGHT)
        self.bgr[1-self.bgr_active].draw(self.surface, 0., self.bgr_offset)
        self.bgr_offset += 1
        if self.bgr_offset == HEIGHT:
            self.bgr[1-self.bgr_active] = Background(self.width, self.height)
            self.bgr_active = 1-self.bgr_active
            self.bgr_offset = 0
        for object in self.targets:
            object.draw(self.surface)
        for object in self.bullets:
            object.draw(self.surface)
        pygame.display.flip()


if __name__=='__main__':
    WIDTH = 1024.
    HEIGHT = 768.
    game = Game(WIDTH, HEIGHT)
    while 1:
        before = time.clock()
        game.update()
        game.draw()
        after = time.clock()
        event = pygame.event.poll()
        if event.type is pygame.KEYDOWN and event.key is pygame.K_ESCAPE:
            exit(0)
        TIME_PERIOD = 0.01
        if after-before < TIME_PERIOD:
            time.sleep(TIME_PERIOD-(after-before))
        else:
            print("Not enough time: " + str(after - before))
