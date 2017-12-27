#!/usr/bin/python
from pygame import *

init()
pantalla = display.set_mode((0, 0), FULLSCREEN)
ww, hh = pantalla.get_size()
imagen = image.load('trashcan_empty.png')
clic = mixer.Sound('menu_click.wav')

xx, yy = 0, hh/2
while True:
    ev = event.poll()
    if ev.type in (QUIT, MOUSEBUTTONDOWN):
        break
    elif ev.type == MOUSEMOTION:
        _, yy = ev.pos                  # posicion
        continue
    time.delay(33)

    xx += 23
    if xx > ww:
        xx -= ww
        clic.play()                     # empezar sonido

    pantalla.fill(0)
    pantalla.blit(imagen, (xx, yy))
    display.flip()
