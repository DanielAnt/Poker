import sys,pygame
from player import *
from board import *
from cards import *

pygame.init()

size = width, height = 1600, 900
speed = [2, 2]
black = 0, 128, 0

screen = pygame.display.set_mode(size)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()


    screen.fill(black)
    pygame.display.flip()


















