#!/usr/bin/env python

import pycozmo


with pycozmo.connect() as cli:

    # Set volume to ~75%.
    cli.set_volume(50000)

    # A 22 kHz, 16-bit, mono file is required.
    cli.play_audio("hello.wav")
    cli.wait_for(pycozmo.event.EvtAudioCompleted)
