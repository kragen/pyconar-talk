#!/usr/bin/python
"""Triangulo de sierpinski por IFS inverso.
"""
import Numeric, pygame, random

pantalla = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
ww, hh = pantalla.get_size()

transforms = [lambda x, y: (x * 2 - ww/2,        y * 2 - 1 * hh/5),
              lambda x, y: (x * 2 - ww/2 - hh/2, y * 2 - 4 * hh / 5),
              lambda x, y: (x * 2 - ww/2 + hh/2, y * 2 - 4 * hh / 5),
# descomentar para efectos alucinantes:
#              lambda x, y: (x * 2 - ww/2,       -y * 2 + 8 * hh/5),
#              lambda x, y: (y * 2 - ww/2,       -x * 2 + 8 * hh/5),
              ]

xs, ys = Numeric.indices((ww, hh))

bounded_coords = []
for transform in transforms:
    xps, yps = transform(xs, ys)

    in_bounds = Numeric.logical_and(
        Numeric.logical_and(xps >= 0, xps < ww),
        Numeric.logical_and(yps >= 0, yps < hh))

    bounded_coords.append((Numeric.where(in_bounds, xps, xs),
                           Numeric.where(in_bounds, yps, ys),
                           in_bounds))

lower_bounds = Numeric.zeros((ww, hh))

def hsva(hh, ss, vv, aa):
    rv = pygame.Color(0)
    rv.hsva = hh, ss, vv, aa
    return int(rv)

hues = [random.randrange(360) for ii in range(3)]
palette = [hsva(random.choice(hues),
                random.randrange(25, 100),
                random.randrange(0, 100),
                100)
           for ii in range(500)]

def take2(pixels, xx, yy):
    ww, hh = pixels.shape
    return Numeric.take(Numeric.reshape(pixels, (ww*hh,)), xx * hh + yy)

while True:
    ev = pygame.event.poll()
    if ev.type in (pygame.QUIT, pygame.MOUSEBUTTONDOWN):
        break
    elif ev.type != pygame.NOEVENT:
        continue
    
    pygame.surfarray.blit_array(pantalla, Numeric.take(palette, lower_bounds))
    pygame.display.flip()

    new_lower_bounds = lower_bounds
    for xps, yps, in_bounds in bounded_coords:
        new_lower_bounds = Numeric.where(in_bounds,
                                         Numeric.maximum(
                                             take2(lower_bounds, xps, yps) + 1,
                                             new_lower_bounds),
                                         new_lower_bounds)

    lower_bounds = new_lower_bounds
