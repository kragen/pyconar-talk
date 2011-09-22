#!/usr/bin/python
from pygame import *
from random import randrange

pantalla = display.set_mode((0, 0), FULLSCREEN)
ww, hh = pantalla.get_size()

for xx in range(0, ww, 5):
    draw.line(pantalla,
              (64, 64, 192),
              (xx, 20),
              (randrange(ww), hh - 20),
              10)
    display.flip()
