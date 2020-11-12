#!/usr/bin/env python

import time

import pycozmo


with pycozmo.connect() as cli:

    cli.set_head_angle(pycozmo.MAX_HEAD_ANGLE.radians)
    time.sleep(1)
    cli.set_head_angle(pycozmo.MIN_HEAD_ANGLE.radians)
    time.sleep(1)

    cli.set_lift_height(pycozmo.MAX_LIFT_HEIGHT.mm)
    time.sleep(1)
    cli.set_lift_height(pycozmo.MIN_LIFT_HEIGHT.mm)
    time.sleep(1)
