import pygame

from setup import *
from dungeon import *
from utils import *


from random import randint
from enum import Enum

pygame.init()
pygame.display.set_caption("Mazerr")




# TODO replace coordinant separation by self.get(coords)


new_maze = Maze()

pretty_print(new_maze.board)


while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                new_maze.player.move('U')
            elif event.key == pygame.K_DOWN:
                new_maze.player.move('D')
            elif event.key == pygame.K_LEFT:
                new_maze.player.move('L')
            elif event.key == pygame.K_RIGHT:
                new_maze.player.move('R')

    screen.fill(DEEP_PURPLE)
    new_maze.draw()
    pygame.display.flip()

    clock.tick(60)
