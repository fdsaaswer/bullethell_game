import pygame
import time

from game import Game

from player import Action
key2action = {  # update in options
    pygame.K_SPACE: Action.ATTACK,
    pygame.K_LEFT: Action.MOVE_LEFT,
    pygame.K_RIGHT: Action.MOVE_RIGHT,
    pygame.K_UP: Action.MOVE_UP,
    pygame.K_DOWN: Action.MOVE_DOWN
}

if __name__=='__main__':
    WIDTH = 1024
    HEIGHT = 768
    game = Game(WIDTH, HEIGHT)
    while 1:
        before = time.clock()
        game.update()
        game.draw()
        after = time.clock()
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit(0)
            try:
                game.player.action |= key2action[event.key]
            except KeyError:
                pass
        if event.type == pygame.KEYUP:
            try:
                game.player.action &= ~key2action[event.key]
            except KeyError:
                pass
        TIME_PERIOD = 0.01
        if after-before < TIME_PERIOD:
            time.sleep(TIME_PERIOD-(after-before))
        else:
            print("Not enough time: " + str(after - before))
