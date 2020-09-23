#!/usr/bin/env python

import pycozmo


def pycozmo_program(cli: pycozmo.client.Client):

    pkt = pycozmo.protocol_encoder.SetRobotVolume(50000)
    cli.conn.send(pkt)

    # A 22 kHz, 16-bit, mono file is required.
    cli.play_audio("hello.wav").wait_until_complete()


pycozmo.run_program(pycozmo_program)
