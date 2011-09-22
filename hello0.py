#!/usr/bin/python
from pygame import *
from random import randrange

pantalla = display.set_mode((0, 0), FULLSCREEN)
ww, hh = pantalla.get_size()

for xx in range(0, ww, 20):
    draw.line(pantalla,                 # surface
              (64, 64, 192),            # color
              (xx, 20),                 # punto de inicio
              (randrange(ww), hh - 20), # punto de terminar
              10)                       # ancho de rayo
    display.flip()
