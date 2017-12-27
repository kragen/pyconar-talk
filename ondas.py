#!/usr/bin/python

# Simple wave mechanics in PyGame, by Kragen Javier Sitaker, 2007-12-07.

# Needs Python, SDL, PyGame, and Numeric Python installed.

# Notes on speed:

# Sadly at first I was only able to render <17fps with a single wave,
# which means it's doing under 1.3 million pixels per second on my
# 700MHz PIII-Coppermine, and 11fps with two waves.  I thought it was
# absurd that it takes more than 500 clock cycles per pixel,
# especially given that it's not doing any significant amount of
# Python (it's doing about 80 Python bytecodes in the redraw function,
# which adds up to 960 pixels per Python bytecode) but I wrote a C
# version (just doing all the math inside the loop, instead of in big
# arrays) and it was only 50% faster.  After some experimentation, I
# switched the C version to avoid floating-point math in the inner
# loop, to approximate the square root with linear interpolation, and
# to replace the sine function and scaling to palette index operations
# with a table lookup, and quadrupled its speed, making it about six
# times as fast as this Python version at the time.  I tried the same
# optimizations on this program, and it got slower.

# I finally got to 20fps (with one wave) (19% of the C version's
# speed) by switching to single-precision float math.  The tricky
# parts were that single-precision isn't precise enough to express the
# current time (so you have to take it mod 2*pi) and that you have to
# manually convert each scalar to a single-precision float.

import pygame, sys, numpy, time, math

twopi = 2 * math.pi

def grayscale_for_masks(masks, level):
    "Compute a grayscale pixel from bit masks and a floating-point level [0,1)"
    return sum([int(mask * level) & mask for mask in masks])

class World:
    "The stuff that gets drawn on the screen."
    def __init__(self, screen):
        self.screen = screen
        width, height = self.screen.get_size()
        # This is a bit hard to explain, but this makes arrays 'xs'
        # and 'ys' that contain the x and y coordinates of each pixel.
        # So every row of the 'xs' array is [0, 1, 2, 3...], and row 0
        # of the 'ys' array is [0, 0, 0, 0...], while row 1 is [1, 1,
        # 1, 1...].  This is somewhat confused by the default Python
        # display of these guys being transposed if you print them out.
        (self.xs, self.ys) = (xs, ys) = numpy.indices((width, height))
        # Now we want an array of radii (hi Andy).  So we 
        from_center_x = xs - width / 2
        from_center_y = ys - height / 2
        self.r = (numpy.sqrt(from_center_x ** 2 + from_center_y ** 2)
                        /
                  (width/64)).astype(numpy.float32)
        self.tmp = self.r.copy()  # temp space for later (to reduce per-frame allocation)

        masks = self.screen.get_masks()[0:3]
        # Lookup table for grayscale levels.
        self.palette = numpy.array([grayscale_for_masks(masks, level/256.0)
                                        for level in range(256)])
    def add_second_wave(self, to_what): pass
    def peak(self): return 1.01  # was getting occasional overflow errors on y1
    def redraw(self):
        # This function is written in a fairly assembly-language style
        # in order to cut down on the number of intermediate result
        # spaces that must be allocated.
        tmp = self.tmp                  # to make code briefer
        N = numpy
        f32 = lambda x: N.array(x, N.float32)
        # tmp gets -time.time() + self.r
        N.add(f32(-time.time() % twopi), self.r, tmp)
        # tmp gets sin(tmp), i.e. sin(r - time)
        N.sin(tmp, tmp)
        self.add_second_wave(tmp)  # add a second wave in the subclass
        # tmp gets tmp + peak, i.e. peak + sin(r - time)
        N.add(tmp, f32(self.peak()), tmp)
        # tmp gets tmp * (256/ (2*peak)), i.e. (1 + sin(r-time))/2 * 256
        N.multiply(tmp, f32(256 / (self.peak()*2)), tmp)
        # round floats to Int8 so we can look things up in palette
        ints = tmp.astype(N.int8)
        # Look up the pixel value for each grayscale level in the palette
        grayscale = N.take(self.palette, ints)
        # I tried using surfarray.pixels2d and blitting from there,
        # but that made things like 10% slower.  So here we blit_array
        # onto the screen.
        pygame.surfarray.blit_array(self.screen, grayscale)

class World2Waves(World):
    def __init__(self, screen):
        World.__init__(self, screen)
        # Center our second set of waves at the upper left-hand corner
        # of the screen instead of the middle, and give it twice as
        # long a wavelength
        self.r2 = (numpy.sqrt(self.xs ** 2 + self.ys ** 2)
                              /
                   (screen.get_width()/32)).astype(numpy.float32)
        self.tmp2 = self.r.copy()
    def add_second_wave(self, to_what):
        # our second wave travels slower by a factor of e
        numpy.add(numpy.array(-time.time() / numpy.e % twopi,
                              numpy.float32),
                    self.r2, self.tmp2)
        numpy.sin(self.tmp2, self.tmp2)
        numpy.add(self.tmp2, to_what, to_what)
    def peak(self): return 2

def main(argv):
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.mouse.set_visible(False)

    buf = pygame.Surface((256, 150))
    world = World2Waves(buf)  # alternatively just World(screen)
    frames = 0
    start = time.time()
    while 1:
        ev = pygame.event.poll()
        if ev.type == pygame.NOEVENT:
            frames += 1
            world.redraw()
            pygame.transform.smoothscale(buf, screen.get_size(), screen)
            pygame.display.flip()
        elif ev.type == pygame.MOUSEBUTTONDOWN: break
        elif ev.type == pygame.QUIT: break
    end = time.time()
    print "%.2f seconds, %.2f fps" % ((end - start), frames / (end - start))

if __name__ == '__main__': main(sys.argv)
