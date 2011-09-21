#!/usr/bin/python
import pygame, random

ww, hh = 1024, 600
pantalla = pygame.display.set_mode((ww, hh), pygame.FULLSCREEN)

color = pygame.Color(64, 64, 192)
for xx in range(0, ww, 20):
    h, s, v, a = color.hsva
    color.hsva = xx * 270 / ww, s, v, a
    pygame.draw.line(pantalla,
                     color,
                     (xx, 20),
                     (random.randrange(ww), hh - 20),
                     10)
    pygame.display.flip()
