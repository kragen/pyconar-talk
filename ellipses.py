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
                 Rect((0, 0), (ss/2, ss/4)))
    draw.rect(surface, Color(0, 0, 0, 32), surface.get_rect(), 1)
    circles.append((surface, { 'x': rand(ww),  'y': rand(hh), 'theta': 0 }))

pantalla.fill(128)
while event.poll().type not in (QUIT, MOUSEBUTTONDOWN):
    for surface, estado in circles:
        pantalla.blit(transform.rotate(surface, estado['theta']),
                      (estado['x'], estado['y']))
        estado['theta'] += 2            # 2 grados de 360
    display.flip()
