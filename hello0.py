#!/usr/bin/python
import pygame, random

ww, hh = 1024, 600
pantalla = pygame.display.set_mode((ww, hh), pygame.FULLSCREEN)

for xx in range(0, ww, 20):
    pygame.draw.line(pantalla,
                     (64, 64, 192),
                     (xx, 20),
                     (random.randrange(ww), hh - 20),
                     10)
    pygame.display.flip()
