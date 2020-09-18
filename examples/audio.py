#!/usr/bin/env python

import pycozmo


def pycozmo_program(cli: pycozmo.client.Client):

    pkt = pycozmo.protocol_encoder.SetRobotVolume(50000)
    cli.conn.send(pkt)

    cli.play_audio("hello.wav").wait_until_complete()


pycozmo.run_program(pycozmo_program)
