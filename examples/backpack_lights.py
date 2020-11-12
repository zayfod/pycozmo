#!/usr/bin/env python

import time

import pycozmo


with pycozmo.connect() as cli:

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
