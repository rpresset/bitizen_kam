#!/usr/bin/python

import random
import sys
import shutil
import time
import os

EXEC_PATH = os.path.dirname(os.path.abspath(__file__))

CHAR_NAME = 'Frog_Suit'

PAUSEIMG = os.path.join(EXEC_PATH, "images/{0}/{0}_pause.jpg".format(CHAR_NAME))
BLINKIMG = os.path.join(EXEC_PATH, "images/{0}/{0}_blink.jpg".format(CHAR_NAME))
SCRATCH1 = os.path.join(EXEC_PATH, "images/{0}/{0}_scratch1.jpg".format(CHAR_NAME))
SCRATCH2 = os.path.join(EXEC_PATH, "images/{0}/{0}_scratch2.jpg".format(CHAR_NAME))


def blink():
    for i in range(2):
        shutil.copyfile(BLINKIMG, os.path.join(EXEC_PATH, "images/VID_{:02d}.jpg".format(i)))
    time.sleep(0.1)
    for i in range(2):
        shutil.copyfile(PAUSEIMG, os.path.join(EXEC_PATH, "images/VID_{:02d}.jpg".format(i)))

def scratch():
    shutil.copyfile(SCRATCH1, os.path.join(EXEC_PATH, "images/VID_00.jpg"))
    shutil.copyfile(SCRATCH2, os.path.join(EXEC_PATH, "images/VID_01.jpg"))
    time.sleep(0.7)
    for i in range(2):
        shutil.copyfile(PAUSEIMG, os.path.join(EXEC_PATH, "images/VID_{:02d}.jpg".format(i)))

def listen():
    funcs = [scratch, blink, blink]
    while True:
        try:
            time.sleep(random.randrange(2,20))
            random.choice(funcs)()
        except KeyboardInterrupt:
            print '\nExiting blink...'
            for i in range(2):
                shutil.copyfile(PAUSEIMG, os.path.join(EXEC_PATH, "images/VID_{:02d}.jpg".format(i)))
            print 'Clean copy done.'
            return


if __name__ == "__main__":
    listen()
    sys.exit()
