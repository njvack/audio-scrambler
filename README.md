audio-scrambler
===============

A set of python programs to record an endless loop of audio and play it back randomly

Overview
========

The problem at hand: record audio for the last 24 hours, and then play back random, one-second clips of it in a shoutcast stream.

Programs
========

record-ring

Continually records audio to a disk-based ring buffer. At the start of the file, tracks the position that's currently being recorded.

random-playback

Continually seeks within the file written by record-ring and plays segments.
