#!/usr/bin/python
from pygame import *
from random import randrange

pantalla = display.set_mode((0, 0), FULLSCREEN)
ww, hh = pantalla.get_size()

color = Color(64, 64, 192)

for xx in range(0, ww, 5):
    h, s, v, a = color.hsva
    color.hsva = xx * 270 / ww, s, v, a # cambiar hue

    draw.line(pantalla,                 # surface
              color,
              (xx, 20),                 # punto de inicio
              (randrange(ww), hh - 20), # punto de terminar
              10)                       # ancho de rayo
    display.flip()                      # para mostrar
