#!/usr/bin/python
from pygame import *
from random import randrange as rand

pantalla = display.set_mode((0, 0), FULLSCREEN)
ww, hh = pantalla.get_size()

circles = []
for ii in range(20):
    ss = rand(500)
    surface = Surface((ss, ss), SRCALPHA)
    draw.ellipse(surface,
                 Color(rand(256), rand(256), rand(256), 32),
                 surface.get_rect())
    circles.append((surface, { 'x': rand(ww),  'y': rand(hh),
                              'dx': rand(10), 'dy': rand(10)}))

while event.poll().type not in (QUIT, MOUSEBUTTONDOWN):
    for surface, estado in circles:
        pantalla.blit(surface, (estado['x'], estado['y']))
        estado['x'] = (estado['x'] + estado['dx']) % ww
        estado['y'] = (estado['y'] + estado['dy']) % hh
    display.flip()
