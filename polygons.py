#!/usr/bin/python
# basado en
# http://lists.canonical.org/pipermail/kragen-hacks/2008-January/000477.html
from pygame import *
from math import pi, sin, cos

pantalla = display.set_mode((0, 0), FULLSCREEN)
ww, hh = pantalla.get_size()
color, d_d_theta, r = (255, 64, 64), pi/40, hh/2
d_theta = 0

while event.poll().type not in (MOUSEBUTTONDOWN, QUIT):
    d_theta += d_d_theta

    puntos = [(ww/2 + sin(ii * d_theta) * r,
               hh/2 - cos(ii * d_theta) * r)
              for ii in range(3 + d_theta // (2 * pi))]

    pantalla.fill(0)
    draw.polygon(pantalla, color, puntos)

    display.flip()
