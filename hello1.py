#!/usr/bin/python
from pygame import *
from random import randrange

pantalla = display.set_mode((0, 0), FULLSCREEN)
ww, hh = pantalla.get_size()

color = Color(64, 64, 192)
for xx in range(0, ww, 20):
    h, s, v, a = color.hsva
    color.hsva = xx * 270 / ww, s, v, a
    draw.line(pantalla,
              color,
              (xx, 20),
              (randrange(ww), hh - 20),
              10)
    display.flip()
