#!/usr/bin/python
from pygame import *
import random
pantalla = display.set_mode((0, 0), FULLSCREEN)

while event.poll().type not in (QUIT, MOUSEBUTTONDOWN):
    draw.rect(pantalla, random.randrange(2**24), (50, 100, 200, 400))
    display.flip()

