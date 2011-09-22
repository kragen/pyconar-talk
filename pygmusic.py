#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Pygmusic: A simple music sequencer in PyGame.  By Kragen Sitaker,
2007-12-07, 08, 09, 10, 11, and 12.

Drag things around with the mouse; the right mouse button exits.

I, the copyright holder of this work, hereby release it into the
public domain. This applies worldwide.

In case this is not legally possible, I grant any entity the right
to use this work for any purpose, without any conditions, unless
such conditions are required by law.
"""

import pygame, time, os, sys, math

### basic utility functions

def gray(x):
    "Return a grayscale color tuple given an argument in [0,256)"
    return (x, x, x)
black = gray(0)
white = gray(255)

def padd((x1, y1), (x2, y2)):
    "Add an offset to a 2D point."
    return (x2 + x1, y2 + y1)
def pdiff((x1, y1), (x2, y2)):
    "Take the offset between two 2D points."
    return (x2 - x1, y2 - y1)
def pscale((x, y), factor):
    "Scale an offset between two 2-D points by a fraction."
    return (x * factor, y * factor)

### basic drawable objects

class Visible:
    """Things that get drawn on the screen and maybe handle mouse clicks
    or make sounds.

    These objects can be added to the world with world.add and are
    expected to be able to do the following:
    - obj.contains((x, y)): tell whether a mouse position is in the object
    - obj.handle_click(world, event): handle a mouse button going down
    - obj.play(world): make any appropriate sounds
    - obj.center(): return (x, y) center to decide when to be played
    - obj.draw(self, world, screen): display itself; called every frame.
    - obj.is_drop_target_for(self, object, world): handle object being
      dropped on us

    Additionally, if an object is draggable, it needs to support these:
    - obj.move(delta): move by delta x and delta y
    - obj.handle_drop(world): finish being dragged

    In order to use the default implementations of contains and
    center, the object needs to have a rect property that acts like a
    pygame.Rect.

    """
    def contains(self, (x, y)): return self.rect.collidepoint(x, y)
    def center(self): return self.rect.center
    def is_drop_target_for(self, obj, world): "Default is to do nothing."
    def handle_click(self, world, ev): "Default is to do nothing."
    def play(self, world): "Default is to do nothing."

class Timer(Visible):
    "A horizontal strip on the screen that plays things in it when triggered."
    def __init__(self, rect, cycletime, color, active=True, divisions=8):
        "cycletime is the time to go through the whole cycle."
        self.rect = rect
        self.cycletime = cycletime
        self.color = color
        self.active = active
        self.start = time.time()
        self.lastoffset = 0
        self.divisions = divisions
    def drawvbar(self, screen, offset, color):
        "Draws a timing mark at a given offset."
        screen.fill(color, ((self.rect.left + offset, self.rect.top),
                            (1, self.rect.h)))
    def drawvbars(self, screen, n, color):
        "Draw timing marks for odd intervals of every nth of a cycle."
        for ii in range(1, n):
            self.drawvbar(screen, ii * self.rect.w / float(n), color)
    def draw(self, world, screen):
        screen.fill(gray(self.color), self.rect)
        self.drawvbars(screen, self.divisions*2, gray(136))
        self.drawvbars(screen, self.divisions, gray(144))
        self.drawvbars(screen, 2, gray(192))
        if self.active: self.draw_cursor(world, screen)
    def time(self):
        "The time since the beginning of the current play cycle."
        age = time.time() - self.start
        if age > self.cycletime: return self.cycletime
        return age
    def offset(self):
        "The current position of the cursor for this timer."
        return int(self.time() / self.cycletime * self.rect.w + 0.5)
    def handle_click(self, world, ev): self.trigger()
    def trigger(self):
        "Start playing the sounds within."
        self.active = True
        self.lastoffset = 0
        self.start = time.time()
    def triggerpoint(self):
        return self.rect.midleft
    def cursor_rect(self, start, end):
        "Returns a Rect from pixel offset 'start' to 'end' for a cursor."
        return pygame.Rect((self.rect.left + start, self.rect.top),
                           (end - start, self.rect.h))
    def cursor_rects(self, offset):
        "Returns the Rects showing the currently playing period on the screen."
        assert offset >= self.lastoffset
        return [self.cursor_rect(self.lastoffset, offset)]
    def draw_cursor(self, world, screen):
        """Draws the white box that represents the currently playing period,
        and also plays the sounds found within."""
        offset = self.offset()
        for rect in self.cursor_rects(offset):
            screen.fill(white, rect)
            # If we .play() things immediately, there could be
            # surprising effects (e.g. if we're playing ourselves).
            # So we enqueue the playing for later.
            for obj in world.objects_in(rect):
                world.defer(lambda obj=obj: obj.play(world))
        self.lastoffset = offset

class RepeatingTimer(Timer):
    "A horizontal strip on the screen that plays things in it repeatedly."
    def time(self):
        return (time.time() - self.start) % self.cycletime
    def handle_click(self, world, ev):
        "Turns the timer on and off when clicked."
        if not self.active: self.lastoffset = self.offset()
        self.active = not self.active
    def cursor_rects(self, offset):
        if offset >= self.lastoffset:
            return [self.cursor_rect(self.lastoffset, offset)]
        else:
            return [self.cursor_rect(self.lastoffset, self.rect.w),
                    self.cursor_rect(0, offset)]

class ImageDisplay(Visible):
    "A visible object that displays by merely blitting an image."
    def __init__(self, pos, image):
        self.image = image
        self.rect = pygame.Rect(pos, image.get_size()) # to satisfy Visible
    def draw(self, world, surface):
        "ImageDisplay.draw just blits the object's image."
        surface.blit(self.image, self.rect.topleft)

class UglyHalo(ImageDisplay):
    """A white square that fades to nothing over 0.6 seconds to show
    that something has happened."""
    def __init__(self, rect):
        "rect is the area to draw the halo around."
        halosize = rect.h * 2
        # I wanted to do a circle, but it turns out that in SDL you can't
        # have both a per-pixel alpha and a per-surface alpha, and I
        # figured that fading the per-pixel alpha in a Python nested loop
        # would be too slow, so for now, it's a white square.  See the
        # NumericHalo class for an alternative.
        image = pygame.surface.Surface((halosize, halosize))
        image.fill(white)
        ImageDisplay.__init__(self, pdiff(image.get_rect().center, rect.center),
                              image)
        self.start = time.time()
    def draw(self, world, surface):
        "Blits the halo image with the current opacity; possibly suicides."
        age = time.time() - self.start
        opacity = int(255 * (0.6 - age))
        if opacity <= 0: world.delete(self)
        else:
            self.image.set_alpha(opacity)
            ImageDisplay.draw(self, world, surface)

### rendering haloes with Numeric

def scale(mask, component):
    "Encode a floating-point color component in [0, 1] with a bitmask."
    assert 0 <= component <= 1, component
    mask = mask % (2**32)               # make unsigned
    rv = int(mask * component) & mask   # scale mask by weight
    if rv >= 2**31: rv -= 2**32         # convert back to signed
    rv = int(rv)                        # convert back to non-long
    return rv

def pixel(masks, components):
    "Encode an (r, g, b, alpha) tuple according to given masks."
    return sum(map(scale, masks, components))

class NumericHaloMovie:
    "Renders frames of a halo on demand, then caches them."
    def __init__(self, args):
        framelength, size, max_age, fuzz = args
        self.framelength = framelength
        self.size = size                # size of the object halo is around
        self.max_age = max_age
        self.fuzzsq = fuzz**2
        self.frames = {}
        self.shape = (size*2, size*2)
        cx = cy = size                  # x and y at center
        xs, ys = Numeric.indices(self.shape) # x and y coords of each pixel
        (dx, dy) = (xs - cx, ys - cy)   # distances from center for each pixel
        self.rsq = dx*dx + dy*dy        # squared distance from center
    def render_frame(self, framenum):
        age = framenum * self.framelength # age in seconds to show this frame at
        # create a surface that has an alpha channel, to render to and return
        mysurf = pygame.Surface(self.shape).convert_alpha()
        masks = mysurf.get_masks()      # get bitmasks for r, g, b, alpha
        global_alpha = (self.max_age**2 - age**2)/self.max_age**2
        fsq = self.fuzzsq
        # palette is the colors in delta-rsquared, from densest to
        # most rarefied.  Most rarefied is transparent, 0.  Densest is
        # nearly white.
        palette = Numeric.array(
            [pixel(masks, (1, 1,        # r and g are always 100%
                           0.8 * float(fsq-ii)/fsq, # b is 0-80%
                           0.9 * float(fsq-ii)/fsq * global_alpha))
             for ii in range(fsq)] + [0])
        # This is the r-squared where that maximum density is found.
        # The formula is just voodoo --- I whacked on it until the
        # effect looked OK.  It doesn't scale properly with max_age.
        max_level = self.size**2/2 * (1 - (1 - age*2)**2)
        # Take absolute difference of r-squared from the point of the
        # current maximum, clamp it between 0 and fuzz**2, convert to
        # integer so we can use it to index the palette.
        density = Numeric.clip(Numeric.absolute(self.rsq - max_level),
                               0, fsq).astype(Numeric.Int)
        colors = Numeric.take(palette, density)
        pygame.surfarray.blit_array(mysurf, colors)
        return mysurf
    def __getitem__(self, framenum):
        "Get a frame."
        try: return self.frames[framenum]
        except KeyError:
            frame = self.render_frame(framenum)
            self.frames[framenum] = frame
            return frame

halo_movies = {}
def get_halo_movie(*args):
    "Find a requested halo movie."
    # This way multiple haloes of the same size (and other attributes)
    # can share the same rendered frames.
    if halo_movies.has_key(args): return halo_movies[args]
    halo_movies[args] = NumericHaloMovie(args)
    return halo_movies[args]

class NumericHalo(Visible):
    "Draws a fading halo computed with Numerical Python."
    def __init__(self, rect):
        "rect is the area to draw the halo around."
        fuzz = 10
        self.framelength = 1/120.0      # of a second.
        self.max_age = 0.4              # of a second
        self.frames = get_halo_movie(self.framelength, rect.h,
                                     self.max_age, fuzz)
        pos = pdiff(self.frames[0].get_rect().center, rect.center)
        self.rect = pygame.Rect(pos, self.frames[0].get_size())
        self.start = time.time()
    def draw(self, world, surface):
        "Blits the best frame for the halo's current age; possibly suicides."
        age = time.time() - self.start
        if age > self.max_age: world.delete(self)
        else:
            surface.blit(self.frames[int(age / self.framelength + 0.5)],
                         self.rect.topleft)

try:
    # test to see if Numeric and surfarray are available
    import Numeric
    pygame.surfarray.blit_array
except:
    make_halo = UglyHalo
else:
    make_halo = NumericHalo

### Sound-making objects

class DragSource(ImageDisplay):
    "Here is a source you can drag new Visibles from."
    def __init__(self, pos, image, instance):
        "instance is a callable to call with (x, y) to make the new thing."
        ImageDisplay.__init__(self, pos, image)
        self.instance = instance
    def handle_click(self, world, ev):
        "Start a drag with a new instance of, say, a Sound."
        new = self.instance(self.rect.topleft)
        world.add(new)
        new.start_drag(world, ev)
        new.play(world)
        # This (15, 15) offset has four purposes:
        # - it makes it clear that the new thing is a new thing, and
        #   not a change of color of the old thing;
        # - it happens to put that thing by default into one of the
        #   timers, so that if you don't drag it anywhere, it will still
        #   get played.
        # - it suggests the action of dragging (people seem to take a
        #   while to discover the draggability)
        # - it discourages rapid repeat clicking on drag sources,
        #   which tends to create an unwieldy number of objects
        #   without the user noticing.
        ScriptedDrag(world, (15, 15), duration=0.2).run()

class ScriptedDrag:
    def __init__(self, world, delta, duration):
        self.world = world
        self.delta = delta
        self.start = self.lastrun = time.time()
        self.duration = duration
        self.last_offset = (0, 0)
        world.prevent_button_release()
    def run(self):
        now = time.time()
        if now - self.start >= self.duration:
            self.world.defer(self.world.allow_button_release)
            now = self.start + self.duration
        else:
            self.world.defer(self.run)
        # 3t**2 - 2t**3 goes from (0, 0) to (1, 1) with a zero
        # derivative at both points
        t = (now - self.start) / self.duration
        frac = 3*t**2 - 2*t**3
        # We round here to avoid being dependent on PyGame's rounding,
        # and we keep track of the last offset to compensate for the
        # rounding errors.
        (new_x, new_y) = pscale(self.delta, frac)
        new_offset = (int(new_x + 0.5), int(new_y + 0.5))
        delta = pdiff(self.last_offset, new_offset)
        self.last_offset = new_offset
        # This avoids taking mouse control away from the user
        # entirely.
        pygame.mouse.set_pos(padd(pygame.mouse.get_pos(), delta))
        self.lastrun = now

class Sound(ImageDisplay):
    "A draggable sound that you can put in the tracks."
    def __init__(self, pos, image, sound):
        ImageDisplay.__init__(self, pos, image)
        self.sound = sound
    def move(self, delta): self.rect = self.rect.move(delta)
    def start_drag(self, world, ev):
        world.raise_to_top(self)
        world.grab(self, ev.pos)
    def handle_drop(self, world):
        "Handle being dropped; called by the world."
        # we cheat and look a pixel up and left
        droptarget = world.object_at(padd(self.rect.topleft, (-1, -1)))
        if droptarget: droptarget.is_drop_target_for(self, world)
    def handle_click(self, world, ev):
        self.start_drag(world, ev)
        self.play(world)
    def play(self, world):
        "Plays the object's sound and kicks off a halo; called by timer."
        self.sound.play()
        world.add_nonclickable(make_halo(self.rect))

class Trigger(Sound):
    """A draggable object that you can put in a timer to trigger some
    other thing, such as another timer."""
    # XXX currently inherits from Sound so as to be draggable.
    def __init__(self, pos, image, gun):
        ImageDisplay.__init__(self, pos, image)
        self.gun = gun
    def play(self, world):
        world.add_nonclickable(make_halo(self.rect))
        self.gun.trigger()
        world.add_nonclickable(Line(self.center(), self.gun.triggerpoint(),
                                    duration=0.2))

class Line(ImageDisplay):
    # XXX not antialiased and doesn't fade
    # neither pygame.draw.aaline nor pygame.draw.line supports the
    # alpha channel the way one might expect
    def __init__(self, start, end, duration):
        self.start = start
        self.end = end
        self.rect = pygame.Rect(start, pdiff(start, end))
        self.rect.normalize()
        self.starttime = time.time()
        self.duration = duration
    def draw(self, world, surface):
        now = time.time()
        if now > self.starttime + self.duration: world.delete(self)
        else: pygame.draw.line(surface, white, self.start, self.end)

### miscellaneous including the world

class Trash(ImageDisplay):
    """The trashcan deletes things dropped on it."""
    def is_drop_target_for(self, object, world):
        "Delete the dropped thing and make a halo."
        world.delete(object)
        world.add_nonclickable(make_halo(self.rect))

class Profiler:
    def __init__(self):
        self.times = {}
    def __str__(self): return str(self.times)
    def start(self): self.last_time = time.time()
    def note(self, what):
        now = time.time()
        dur = now - self.last_time
        self.last_time = now
        if not self.times.has_key(what): self.times[what] = 0
        self.times[what] += dur

class World:
    """Manages the set of stuff you see on the screen and routes
    events.  I think this is basically the Smalltalk MVC Controller."""
    def __init__(self, screen):
        "screen is an SDL/PyGame surface to draw on."
        self.screen = screen
        self.objects = []               # clickable visible objects
        self.nonclickable_objects = []  # halos and such
        self.grab(None, None)           # initialize drag state
        self.redraw_profiler = Profiler()
        self.deferreds = []
        self.queued_release_events = None
    def redraw(self):
        "This gets called whenever there's idle time, i.e. each frame."
        self.screen.fill(black)
        self.redraw_profiler.start()
        for obj in self.objects + self.nonclickable_objects:
            obj.draw(self, self.screen)
            self.redraw_profiler.note(obj.__class__.__name__)
        self.run_deferreds()
    def run_deferreds(self):
        "Run any deferred tasks."
        deferreds = self.deferreds
        # ensure that tasks deferred by deferred tasks don't run until
        # the next frame:
        self.deferreds = []
        for task in deferreds: task()
    def defer(self, task):
        "Enqueue a task to be done as soon as possible after redraw."
        self.deferreds.append(task)
    def add(self, obj):
        "Call to put a new visible, clickable object on the screen."
        self.objects.append(obj)
    def add_nonclickable(self, obj):
        """Like add, but for nonclickable objects above everything.

        I added this for halos because they were accidentally getting
        drawn underneath other screen objects, and they aren't
        supposed to impede the clickability of the objects they're
        haloing around.
        """
        self.nonclickable_objects.append(obj)
    def object_at(self, pos):
        "Return the topmost object at pos, or None."
        # iterate backwards so objects drawn "on top" get first choice
        for ii in range(len(self.objects)-1, -1, -1):
            if self.objects[ii].contains(pos): return self.objects[ii]
    def handle_click(self, ev):
        "Route a click event to the relevant object."
        obj = self.object_at(ev.pos)
        if obj: obj.handle_click(self, ev)
        else: self.ungrab()
    def handle_release(self, ev):
        "Handle a button release event."
        if self.queued_release_events is None:
            self.ungrab()
        else:
            self.queued_release_events.append(ev)
    def handle_motion(self, ev):
        "Handle mouse motion, by doing a mouse drag if needed."
        if self.dragobj is None: return
        self.dragobj.move(pdiff(self.dragpos, ev.pos))
        self.dragpos = ev.pos
    def ungrab(self):
        "Terminate any drag."
        if self.dragobj is not None: self.dragobj.handle_drop(self)
        self.grab(None, None)
    def grab(self, obj, pos):
        "Start dragging some object."
        (self.dragobj, self.dragpos) = (obj, pos)
    def delete(self, obj):
        "Remove a visible object (clickable or not) from the world."
        if obj in self.nonclickable_objects:
            self.nonclickable_objects.remove(obj)
        else:
            self.objects.remove(obj)
    def raise_to_top(self, obj):
        "Move an object to the top of the drawing stack."
        self.delete(obj)
        self.add(obj)
    def objects_in(self, arect):
        """Find all the objects whose centers are in a rectangle.

        This is used by the timer to figure out what to play.
        """
        return [obj for obj in self.objects
                if arect.contains(pygame.Rect(obj.center(), (1, 1,)))]
    # for scripted drags:
    def prevent_button_release(self):
        self.queued_release_events = []
    def allow_button_release(self):
        release_events = self.queued_release_events
        self.queued_release_events = None
        for event in release_events: self.handle_release(event)

def make_icon():
    size = 32
    icon_surface = pygame.Surface((size, size))
    icon_surface.fill(black)
    try:
        halo = get_halo_movie(1/100.0, size/2, 1, 10)[10]
        icon_surface.blit(halo, (0, 0))
    except: pass # maybe we don't have Numeric
    return icon_surface

def main(argv):
    "Main program."
    mydir = os.path.split(argv[0])[0]
    pygame.init()
    pygame.display.set_caption("Pygmusic sequencer")
    screen = pygame.display.set_mode((640, 480), pygame.FULLSCREEN)
    pygame.display.set_icon(make_icon())
    fullscreen = True

    world = World(screen)
    timerwidth = 440
    def timer(y, cycletime, color, active=True):
        world.add(RepeatingTimer(rect=pygame.Rect((100, y), (timerwidth,30)),
                        cycletime=cycletime*0.16667, color=color, active=active,
                        divisions=cycletime))

    font = pygame.font.Font(None, 24)   # use default font, 24 pixels high
    def getsound(soundname):
        path = os.path.join(mydir, soundname + '.wav')
        return pygame.mixer.Sound(path)
    def renderletter(letter, color): return font.render(letter, 1, color)
    def addsource(xpos, letter, soundname):
        image = renderletter(letter, white)
        sound = getsound(soundname)
        make = lambda pos: Sound(pos=pos, image=image, sound=sound)
        source = DragSource(pos=(xpos, 80),
                            image=renderletter(letter, (255, 128, 128)),
                            instance=make)
        world.add(source)
        return lambda pos: world.add(source.instance(pos))

    yy = addsource(100, 'Y', 'score')
    zz = addsource(120, 'Z', 'extraball')
    aa = addsource(140, 'A', 'reflect_paddle')
    bb = addsource(160, 'B', 'reflect_brick')
    addsource(180, 'C', 'menu_click')
    addsource(200, 'D', 'shrink')

    timer(100, 3, 128)
    bb((95, 100))
    timer(130, 5, 120, active=False)
    zz((95, 130))
    timer(160, 7, 128, active=False)
    yy((95, 160))
    timer(190, 8, 120)
    aa((95, 190))
    aa((95 + timerwidth/2, 190))

    mytimer = Timer(rect=pygame.Rect((100, 250), (timerwidth,30)),
                    cycletime=1, color=128, active=True,
                    divisions=6)
    world.add(mytimer)
    world.add(DragSource((75, 250), image=renderletter("E", (255, 128, 128)),
                         instance = lambda pos:
                             Trigger(pos, renderletter("E", white), mytimer)))

    trashf = os.path.join(mydir, 'trashcan_empty.png')
    world.add(Trash((100, 300), pygame.image.load(trashf).convert()))

    # Some basic instructions.
    world.add(ImageDisplay((200, 300),
        font.render("Drag things around with the mouse.", 1, white)))
    world.add(ImageDisplay((200, 320),
        font.render("The right mouse button exits.", 1, white)))

    frames = 0
    start = time.time()
    while 1:
        ev = pygame.event.poll()
        if ev.type == pygame.NOEVENT:
            world.redraw()
            frames += 1
            pygame.display.flip()
        elif ev.type == pygame.MOUSEMOTION:
            world.handle_motion(ev)
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 3: break
            world.handle_click(ev)
        elif ev.type == pygame.MOUSEBUTTONUP:
            world.handle_release(ev)
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    pygame.display.set_mode((640, 480), pygame.FULLSCREEN)
                else:
                    pygame.display.set_mode((640, 480)) # without FULLSCREEN
        elif ev.type == pygame.QUIT: break
    end = time.time()
    print "%.2f seconds, %.2f fps" % ((end - start), frames / (end - start))
    print 'redraw times', world.redraw_profiler

if __name__ == '__main__': main(sys.argv)
