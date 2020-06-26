#!/usr/bin/python

import os
import shutil
import sys
import numpy
import time
import audioop
import alsaaudio
import random
import virtualvideo
import cv2

EXEC_PATH = os.path.dirname(os.path.abspath(__file__))

CHAR_NAME = 'Frog_Suit'

PAUSEIMG = os.path.join(EXEC_PATH, "images/{0}/{0}_pause.jpg".format(CHAR_NAME))
SMILEIMG = os.path.join(EXEC_PATH, "images/{0}/{0}_smile.jpg".format(CHAR_NAME))
TLKIMG = os.path.join(EXEC_PATH, "images/{0}/{0}_talk.jpg".format(CHAR_NAME))
THMBIMG = os.path.join(EXEC_PATH, "images/{0}/{0}_thumbup.jpg".format(CHAR_NAME))
SCRATCH1 = os.path.join(EXEC_PATH, "images/{0}/{0}_scratch1.jpg".format(CHAR_NAME))
SCRATCH2 = os.path.join(EXEC_PATH, "images/{0}/{0}_scratch2.jpg".format(CHAR_NAME))
BLINKIMG = os.path.join(EXEC_PATH, "images/{0}/{0}_blink.jpg".format(CHAR_NAME))

#interactions
SMILE =  "/tmp/chatgif.smile"
THUMB =  "/tmp/chatgif.thumb"

#SETTINGS
CHAR_NAME = 'Frog_Suit'
# animation specifics settings
FRAMERATE = 30 #frames per seconds
THUMB_DURATION = 1 #seconds
SMILE_DURATION = 1 #seconds
SCRATCH_DURATON = 0.7 #seconds
BLINK_FREQUENCY = 8 #hertzs
TALK_FREQUENCY = 12 #hertz
SCRATCH_FREQUENCY = 8 #hertz
#rabdomisation
BLINK_PERCENT = 0.7
SCRATCH_PERCENT = 0.3
# audio_settings
AUDIO_THRESHOLD = 1500


# I am assuming here that I can define the persiod size depending on the rate ans the nb of samples i need.
# doc does not seem to say this, but those presets works for me. Ill understand later...
SAMPLES = 4
AUDIO_RATE = 8000 #Hz

# Open the device in nonblocking capture mode. The last argument could
# just as well have been zero for blocking mode. Then we could have
# left out the sleep call in the bottom of the loop
inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)

# Set attributes: Mono, 8000 Hz, 16 bit little endian samples
inp.setchannels(1)
inp.setrate(AUDIO_RATE)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

# The period size controls the internal number of frames per period.
# The significance of this parameter is documented in the ALSA api.
# For our purposes, it is suficcient to know that reads from the device
# will return this many frames. Each frame being 2 bytes long.
# This means that the reads below will return either 320 bytes of data
# or 0 bytes of data. The latter is possible because we are in nonblocking
# mode.

inp.setperiodsize(AUDIO_RATE/SAMPLES) 

#interactions
SMILE =  "/tmp/chatgif.smile"
THUMB =  "/tmp/chatgif.thumb"


def get_audio_sample(inp):
    sample_length, sample_data = inp.read()
    if sample_length:
        return audioop.max(sample_data, 2)
    else: 
        return 0


class BitizenFeed(virtualvideo.VideoSource):
    def __init__(self):
        self.img = cv2.imread(PAUSEIMG)
        size = self.img.shape
        #opencv's shape is y,x,channels
        self._size = (size[1],size[0])
        self._idle_sequence = []
        self._talk_sequence = []
        self._smile_sequence = []
        self._thumb_sequence = []
        self._blink_sequence = []
        self._scratch_sequence = []

    @property
    def thumb(self):
        """
        TODO: make the  trigger better
        """
        if os.path.isfile(THUMB):
            os.remove(THUMB)
            return True
        else:
            return False
    @property
    def smile(self):
        """
        TODO: make the  trigger better
        """
        if os.path.isfile(SMILE):
            os.remove(SMILE)
            return True
        else:
            return False

    @property
    def idle_sequence(self):
        if not self._idle_sequence:
            self._idle_sequence.append(cv2.imread(PAUSEIMG))
        return self._idle_sequence

    @property
    def talk_sequence(self):
        """
        animation_freq is the frequence of the animation in Hz (1/s)
        Actually not. It seems not working this way. TBD
        """
        if not self._talk_sequence:
            for _ in range(FRAMERATE / TALK_FREQUENCY):
                self._talk_sequence.append(cv2.imread(TLKIMG))
            for _ in range(FRAMERATE / TALK_FREQUENCY):
                self._talk_sequence.append(cv2.imread(PAUSEIMG))
        return self._talk_sequence

    @property
    def smile_sequence(self):
        if not self._smile_sequence:
            for _ in range(FRAMERATE * SMILE_DURATION):
                self._smile_sequence.append(cv2.imread(SMILEIMG))
        return self._smile_sequence

    @property
    def thumb_sequence(self):
        if not self._thumb_sequence:
            for _ in range(FRAMERATE * THUMB_DURATION):
                self._thumb_sequence.append(cv2.imread(THMBIMG))
        return self._thumb_sequence

    @property
    def blink_sequence(self):
        if not self._blink_sequence:
            for _ in range(FRAMERATE / BLINK_FREQUENCY):
                self._blink_sequence.append(cv2.imread(BLINKIMG))
        return self._blink_sequence

    @property
    def scratch_sequence(self):
        if not self._scratch_sequence:
            for _ in range(FRAMERATE / SCRATCH_FREQUENCY):
                self._scratch_sequence.append(cv2.imread(SCRATCH1))
            for _ in range(FRAMERATE / SCRATCH_FREQUENCY):
                self._scratch_sequence.append(cv2.imread(SCRATCH2))
        return self._scratch_sequence

    def img_size(self):
        return self._size

    def fps(self):
        return FRAMERATE

    def get_audio_sample(self, inp):
        sample_length, sample_data = inp.read()
        if sample_length:
            return audioop.max(sample_data, 2)
        else:
            return 0

    def generator(self):
        # idle trigger
        frame = 0
        randomisation_delay = random.randrange(2,20) * FRAMERATE
        while True:
            sample_length, sample_data = inp.read()
            try:
                if sample_length:
                    audio_data = audioop.max(sample_data, 2)
                    # talking trigger
                    if audio_data > AUDIO_THRESHOLD:
                        for img in self.talk_sequence:
                            yield img
                            time.sleep(1.0/FRAMERATE)
                    if audio_data <= AUDIO_THRESHOLD:
                        # smile if triggered
                        if self.smile:
                            smile_frame = 0
                            while smile_frame < FRAMERATE * SMILE_DURATION:
                                for img in self.smile_sequence:
                                    yield img
                                    time.sleep(1.0/FRAMERATE)
                                    smile_frame += 1
                        # thumb up if triggered
                        elif self.thumb:
                            thumb_frame = 0
                            while thumb_frame < FRAMERATE * THUMB_DURATION:
                                for img in self.thumb_sequence:
                                    yield img
                                    time.sleep(1.0/FRAMERATE)
                                    thumb_frame += 1
                        # scratch or blink if it meets randomization
                        elif frame == randomisation_delay:
                            action = numpy.random.choice(['blink', 'scratch'], p=[BLINK_PERCENT, SCRATCH_PERCENT])
                            # blink
                            if action == 'blink':
                                for img in self.blink_sequence:
                                    yield img
                                    time.sleep(1.0/FRAMERATE)
                            # or scratch
                            elif action == 'scratch':
                                scratch_frame = 0
                                while scratch_frame < FRAMERATE * SCRATCH_DURATON:
                                    for img in self.scratch_sequence:
                                        yield img
                                        time.sleep(1.0/FRAMERATE)
                                        scratch_frame += 1
                            frame = 0
                            randomisation_delay = random.randrange(2,20) * FRAMERATE
                        # else idle
                        else:
                            for img in self.idle_sequence:
                                yield img
                                time.sleep(1.0/FRAMERATE)
                                frame += 1
            except KeyboardInterrupt:
                print '\nExiting bitizen_kam...'
                print 'press Ctrl+C again to quit' #why???
                sys.exit()
                return


vidsrc = BitizenFeed()
fvd = virtualvideo.FakeVideoDevice()
fvd.init_input(vidsrc)
fvd.init_output(0, 480, 360, fps=FRAMERATE)
fvd.run()

