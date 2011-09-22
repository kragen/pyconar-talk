#!/usr/bin/python
# basado en
# http://lists.canonical.org/pipermail/kragen-hacks/2007-November/000465.html

from pygame import mixer, sndarray, time, init
from Numeric import arange, Int16, sin, pi
tasa = 22050                            # de muestreo

def sinus(hz, pico, n_muestras):
    theta = arange(n_muestras) * (2*pi * hz / tasa)
    return (pico * sin(theta)).astype(Int16)

mixer.pre_init(tasa, -16, 1)
init()

sonido = None
for ii in range(1, 13):
    hz = 440 * pow(2, ii/12.0)
    n_muestras = 256 * tasa // hz
    muestras = sum(sinus(jj*hz, 4096, n_muestras)
                   for jj in [1, 1, 2, 2, 4, 8, 3, 5, 6][:ii])

    if sonido is not None:
        sonido.fadeout(20)
    sonido = sndarray.make_sound(muestras)
    sonido.play(-1, 1000, 20)
    time.delay(500)

