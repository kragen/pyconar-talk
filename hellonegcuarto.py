#!/usr/bin/python
from pygame import *
import random, math
pantalla = display.set_mode((0, 0), FULLSCREEN)
theta = 0

while event.poll().type not in (QUIT, MOUSEBUTTONDOWN):
    draw.polygon(pantalla, random.randrange(2**24),
                 [(200 + math.sin(ii * math.pi/2 + theta) * 100,
                   200 + math.cos(ii * math.pi/2 + theta) * 100)
                  for ii in range(4)])
    theta += 0.02
    display.flip()
