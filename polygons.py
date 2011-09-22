#!/usr/bin/python
# basado en
# http://lists.canonical.org/pipermail/kragen-hacks/2008-January/000477.html
# lo cual es inspirado por Pedal (1995), por Dave Moore
from pygame import *
from math import pi, sin, cos

pantalla = display.set_mode((0, 0), FULLSCREEN)
ww, hh = pantalla.get_size()
theta, d_theta, r, color = 0, 0.04, hh/2, (255, 64, 64)

while event.poll().type not in (MOUSEBUTTONDOWN, QUIT):
    theta += d_theta

    puntos = [(ww/2 + sin(ii * theta) * r, # x
               hh/2 - cos(ii * theta) * r) # y
              for ii in range(3 + theta // (2 * pi))]

    pantalla.fill(0)                    # llenar con negro
    draw.polygon(pantalla, color, puntos)

    display.flip()
