#!/usr/bin/python
"This does not work."

import pygame, pygame.movie, pygame.display

pygame.init()
screen = pygame.display.set_mode((640, 480), pygame.FULLSCREEN)
tankman = pygame.movie.Movie('tankman.mpeg')
tankman.set_display(screen)
tankman.play()

while tankman.get_busy():
    if pygame.event.poll().type == pygame.MOUSEBUTTONDOWN:
        break
    pygame.display.flip()
