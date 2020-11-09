#!/usr/bin/env python

import pycozmo


def pycozmo_program(cli: pycozmo.client.Client):

    cli.set_volume(50000)

    # A 22 kHz, 16-bit, mono file is required.
    cli.play_audio("hello.wav")
    cli.wait_for(pycozmo.event.EvtAudioCompleted)


pycozmo.run_program(pycozmo_program, enable_procedural_face=False)
