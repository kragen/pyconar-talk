#!/usr/bin/python
# md5sum $(locate -b .wav) | sort | uniq -w 32 | sort -R | awk '{print $2}' | head -36 | while read sound; do cp "$sound" sounds/.; done
from pygame import *
import string, os

init()
pantalla = display.set_mode((100, 100))
sounds = dict((char, mixer.Sound(os.path.join('sounds', fname)))
              for char, fname in zip(string.ascii_lowercase + string.digits,
                                     sorted(os.listdir('sounds'))))

while True:
    ev = event.poll()
    if ev.type in (QUIT, MOUSEBUTTONDOWN):
        break
    elif ev.type == KEYDOWN:
        if ev.unicode in sounds:
            sounds[ev.unicode].play()
