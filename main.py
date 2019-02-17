import pygame
import time

from game import Game

if __name__=='__main__':
    WIDTH = 1024
    HEIGHT = 768
    game = Game(WIDTH, HEIGHT)
    while 1:
        before = time.clock()
        game.update()
        game.draw()
        game.process_event(pygame.event.poll())
        after = time.clock()
        TIME_PERIOD = 0.01
        if after - before < TIME_PERIOD:
            time.sleep(TIME_PERIOD-(after-before))
        else:
            print("Not enough time: " + str(after - before))
