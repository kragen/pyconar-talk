#!/usr/bin/python
import pygame, random

ww, hh = 1024, 600
pantalla = pygame.display.set_mode((ww, hh), pygame.FULLSCREEN)

for xx in range(0, ww, 20):
    pygame.draw.line(pantalla,
                     random.randrange(2**24), # color
                     (xx, 20),
                     (random.randrange(ww), hh - 20),
                     10)
    pygame.display.flip()
