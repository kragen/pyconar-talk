#!/usr/bin/python
from pygame import *
pantalla = display.set_mode((0, 0), FULLSCREEN)
draw.rect(pantalla, 128, (50, 100, 200, 400))
display.flip()
time.delay(2000)
