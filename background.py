from random import random

import pygame


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
    list = [(0., 0., width, height, 0)]
    while list:
        x1, y1, x2, y2, depth = list.pop()
        print(x1, y1, x2, y2, depth)
        if random() < 0.5 and depth < 6:
            y_ = y1 + (y2 - y1)*(random()*0.9 + 0.1)
            list.append((x1, y1, x2, y_, depth + 1))
            list.append((x1, y_, x2, y2, depth + 1))
        elif random() < 0.0 and depth < 6:
            x_ = x1 + (x2 - x1)*(random()*0.9 + 0.1)
            list.append((x1, y1, x_, y2, depth + 1))
            list.append((x_, y1, x2, y2, depth + 1))
        else:
            x1 += 10. + random()*90.
            x2 -= 10. + random()*90.
            y1 += 10. + random()*40.
            y2 -= 10. + random()*40.
            if x2 - x1 > 20. and y2 - y1 > 20.:
                pygame.draw.rect(surface, (0, 0, 0), (x1, y1, x2 - x1, y2 - y1), 1)
                if depth < 6:
                    list.append((x1, y1, x2, y2, depth + 1))

    return surface
