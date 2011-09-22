#!/usr/bin/python
from pygame import *
from random import randrange as rand

pantalla = display.set_mode((0, 0), FULLSCREEN)

circles = []
for ii in range(20):
    ss = rand(500)
    surface = Surface((ss, ss), SRCALPHA)
    draw.ellipse(surface,
                 Color(rand(256), rand(256), rand(256), 128),
                 surface.get_rect())
    circles.append(surface)

while event.poll().type not in (QUIT, MOUSEBUTTONDOWN):
    pantalla.blit(circles[rand(len(circles))],
                  (rand(pantalla.get_width()),   # x
                   rand(pantalla.get_height()))) # y
    display.flip()
