#!/usr/bin/python
# basado en
# http://lists.canonical.org/pipermail/kragen-hacks/2007-November/000465.html

from pygame import mixer, sndarray, time, init
from numpy import arange, int16, sin, pi
tasa = 22050                            # de muestreo

mixer.pre_init(tasa, -16, 1)            # 16bit, un canal
init()                                  # necesario para mixer

hz, pico, n_muestras = 440, 16384, tasa
theta = arange(n_muestras) * (2*pi * hz / tasa)

sndarray.make_sound((pico * sin(theta)).astype(int16)
                    ).play(-1, 0, 20)   # 20ms fadein
time.wait(1000)                         # un segundo
