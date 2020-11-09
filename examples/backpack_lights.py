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
        cli.set_all_backpack_lights(light)
        time.sleep(2)


pycozmo.run_program(pycozmo_program, enable_procedural_face=False)
