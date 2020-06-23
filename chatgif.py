#!/usr/bin/python

import os
import shutil
import sys
import time
import audioop
import alsaaudio


# Open the device in nonblocking capture mode. The last argument could
# just as well have been zero for blocking mode. Then we could have
# left out the sleep call in the bottom of the loop
inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)
#inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL)

# Set attributes: Mono, 8000 Hz, 16 bit little endian samples
inp.setchannels(1)
inp.setrate(8000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

# The period size controls the internal number of frames per period.
# The significance of this parameter is documented in the ALSA api.
# For our purposes, it is suficcient to know that reads from the device
# will return this many frames. Each frame being 2 bytes long.
# This means that the reads below will return either 320 bytes of data
# or 0 bytes of data. The latter is possible because we are in nonblocking
# mode.
inp.setperiodsize(160)

EXEC_PATH = os.path.dirname(os.path.abspath(__file__))

CHAR_NAME = 'Frog_Suit'

PAUSEIMG = os.path.join(EXEC_PATH, "images/{0}/{0}_pause.jpg".format(CHAR_NAME))
SMILEIMG = os.path.join(EXEC_PATH, "images/{0}/{0}_smile.jpg".format(CHAR_NAME))
TLKIMG = os.path.join(EXEC_PATH, "images/{0}/{0}_talk.jpg".format(CHAR_NAME))
THMBIMG = os.path.join(EXEC_PATH, "images/{0}/{0}_thumbup.jpg".format(CHAR_NAME))


#interactions
SMILE =  "/tmp/chatgif.smile"
THUMB =  "/tmp/chatgif.thumb"

def idle():
    shutil.copyfile(PAUSEIMG, os.path.join(EXEC_PATH, "images/VID_01.jpg"))

def talk():
    shutil.copyfile(TLKIMG, os.path.join(EXEC_PATH, "images/VID_01.jpg"))

def smile(duration=1):
    for i in range(2):
        shutil.copyfile(SMILEIMG, os.path.join(EXEC_PATH, "images/VID_{:02d}.jpg".format(i)))
    time.sleep(duration)
    for i in range(2):
        shutil.copyfile(PAUSEIMG, os.path.join(EXEC_PATH, "images/VID_{:02d}.jpg".format(i)))

def thumbup(duration=1):
    for i in range(2):
        shutil.copyfile(THMBIMG, os.path.join(EXEC_PATH, "images/VID_{:02d}.jpg".format(i)))
    time.sleep(duration)
    for i in range(2):
        shutil.copyfile(PAUSEIMG, os.path.join(EXEC_PATH, "images/VID_{:02d}.jpg".format(i)))


def listen(input_audio, threshold=800):
    blah = False
    while True:
        try:
            # Read data from device
            sample_length, sample_data = input_audio.read()
            if sample_length:
                audio_data = audioop.max(sample_data, 2)
                if audio_data > threshold and not blah:
                    talk()
                    blah = True
                elif audio_data <= threshold and blah:
                    idle()
                    blah = False
            if os.path.isfile(SMILE):
                os.remove(SMILE)
                smile()
            if os.path.isfile(THUMB):
                os.remove(THUMB)
                thumbup()
            time.sleep(.01)
        except KeyboardInterrupt:
            print '\nExiting chatgif...'
            for i in range(2):
                shutil.copyfile(PAUSEIMG, os.path.join(EXEC_PATH, "images/VID_{:02d}.jpg".format(i)))
            print 'Clean copy done. Press Ctrl+C again to quit'  #Why???
            return


if __name__ == "__main__":
    listen(inp)
    sys.exit()
