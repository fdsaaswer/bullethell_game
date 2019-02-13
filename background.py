import pygame
from random import random
import collections


class Background:
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._bgr_active = 0
        self._bgr_offset = 0
        self._bgr_surface = [background_surface(width, height),
                             background_surface(width, height)]

    def update(self):
        self._bgr_offset += 1
        if self._bgr_offset == self._height:
            self._bgr_surface[1-self._bgr_active] = background_surface(self._width, self._height)
            self._bgr_active = 1-self._bgr_active
            self._bgr_offset = 0

    def draw(self, surface):
        surface.blit(
            self._bgr_surface[self._bgr_active],
            (0., 0.),
            (0., self._height - self._bgr_offset, self._width, self._height)
        )
        surface.blit(
            self._bgr_surface[1-self._bgr_active],
            (0., self._bgr_offset),
            (0., 0., self._width, self._height - self._bgr_offset)
        )


def background_surface(width, height):
    surface = pygame.Surface((width, height))
    surface.fill((255, 255, 255))
    BackgroundInternal(width, height).draw(surface, 0., 0.)
    return surface


class BackgroundInternal:
    def __init__(self, x, y, depth=0):
        self.x = x
        self.y = y
        self.depth = depth
        self.color = random() * 100.
        self.children = []
        Node = collections.namedtuple("Node", "rect offset_x offset_y")
        if random() < 0.5 and depth < 6:
            offset = y*(random()*0.9 + 0.1)
            self.children.append(Node(rect=BackgroundInternal(x, offset, depth+1),
                                      offset_x=0, offset_y=0))
            self.children.append(Node(rect=BackgroundInternal(x, y-offset, depth+1),
                                      offset_x=0, offset_y=offset))
        elif random() < 0.5 and depth < 6:
            offset = x*(random()*0.9 + 0.1)
            self.children.append(Node(rect=BackgroundInternal(offset, y, depth+1),
                                      offset_x=0, offset_y=0))
            self.children.append(Node(rect=BackgroundInternal(x-offset, y, depth+1),
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
                    self.children.append(Node(rect=BackgroundInternal(width, height, depth + 1),
                                              offset_x=new_x_start, offset_y=new_y_start))

    def draw(self, surface, offset_x, offset_y):
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

