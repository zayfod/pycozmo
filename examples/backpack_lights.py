#!/usr/bin/env python

import time

import pycozmo


def pycozmo_program(cli: pycozmo.client.Client):
    lights = [
        pycozmo.lights.red_light,
        pycozmo.lights.green_light,
        pycozmo.lights.blue_light,
        pycozmo.lights.white_light,
        pycozmo.lights.off_light,
    ]
    for light in lights:
        pkt = pycozmo.protocol_encoder.LightStateCenter(states=(light, light, light))
        cli.send(pkt)

        pkt = pycozmo.protocol_encoder.LightStateSide(states=(light, light))
        cli.send(pkt)

        time.sleep(2)


pycozmo.run_program(pycozmo_program)
