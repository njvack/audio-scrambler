#!/usr/bin/env python
# -*- coding: utf-8 -*-

# A little test of pyaudio

import sys
import pyaudio
import wave
import time
import signal
import logging
logging.basicConfig(level=logging.DEBUG)

CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 2
LOOP_SECONDS = 2
RECORD_SECONDS = 6
WAVE_OUTPUT_FILENAME = "output2.wav"


p = pyaudio.PyAudio()
info = p.get_default_input_device_info()
RATE = int(info['defaultSampleRate'])

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

logging.info("* recording")

outfile = open(WAVE_OUTPUT_FILENAME, 'wb')
wf = wave.open(outfile, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes('')
data_offset = outfile.tell()
def record():
    for i in range(0, RECORD_SECONDS / LOOP_SECONDS):
        outfile.seek(data_offset)
        max_frame = max([wf._nframeswritten, 0])
        for j in range(0, int(RATE / CHUNK * LOOP_SECONDS)):
            logging.debug("File tell: %s Wave tell: %s" %
                (outfile.tell(), wf.tell()))
            data = stream.read(CHUNK)
            wf.writeframesraw(data)
            if i > 0:
                wf._nframeswritten = max_frame #Fool python's wave library


def cleanup():
    logging.info("* done recording")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()
    outfile.close()

def handle_sigint(sig, frame):
    logging.info("Exiting!")
    cleanup()
    sys.exit(0)
signal.signal(signal.SIGINT, handle_sigint)

record()
cleanup()