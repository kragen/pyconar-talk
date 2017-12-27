#!/usr/bin/python
"""Recreation of T$'s Klappquadrat intro in Python with Pygame and Numeric.

This is a recreation of the 64-byte version, and I think 31
instructions.  By contrast, this is 44 lines of code, about 1600
characters.  On the other hand, you can change this from 320x200x256
to, say, 640x480x512 by changing the screensize= and ncolors= lines to
say (640, 480) and 512.

Kragen Javier Sitaker wrote this recreation, but T$ is to credit for
the original intro.

http://canonical.org/~kragen/demo/klappquadrat.html

"""

import pygame, sys
from numpy import zeros, subtract, array, arange, where, take, shape, indices, int64, int32

screensize = (320, 200)
ncolors = 256

def colors(masks, levels):
    "Compute a grayscale pixel from bit masks and a floating-point level [0,1)"
    return sum([int(mask * level) & mask for mask, level in zip(masks, levels)])

def clamp(a, b, c):
    "Threshold b between lower limit a and upper limit c."
    d = where(a < b, b, a)
    return where(d < c, d, c)

def redraw(screen, buf, palette, frames):
    x, y = indices(screensize)
    # this 256 is not ncolors; it's a timing/pacing thing
    buf += ((x + frames) & (y + frames)) >> (frames % 256) >> 3
    buf %= ncolors
    pygame.surfarray.blit_array(screen, take(palette, buf))

def main(argv):
    pygame.init()
    screen = pygame.display.set_mode(screensize, pygame.FULLSCREEN)

    buf = zeros(screensize, int32)
    fiery_rgb_integers = clamp(0, subtract.outer(arange(ncolors) + ncolors/8,
                                                 ((array([0, 1, 2]) * ncolors)
                                                  / 4)),
                               ncolors / 4)
    masks = screen.get_masks()[:3]
    # I'm not sure this palette is exactly right; it only goes to 63
    # in the original...
    palette = array([colors(masks, levels/float(ncolors/4))
                     for levels in fiery_rgb_integers])

    frames = 0
    while 1:
        ev = pygame.event.poll()
        if ev.type == pygame.NOEVENT:
            frames += 1
            redraw(screen, buf, palette, frames)
            pygame.display.flip()
            pygame.time.delay(67)
        elif ev.type == pygame.KEYDOWN: break
        elif ev.type == pygame.QUIT: break

if __name__ == '__main__': main(sys.argv)
