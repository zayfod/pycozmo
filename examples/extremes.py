#!/usr/bin/env python

import time

import pycozmo


def pycozmo_program(cli: pycozmo.client.Client):

    cli.set_head_angle(pycozmo.MAX_HEAD_ANGLE.radians)
    time.sleep(1)
    cli.set_head_angle(pycozmo.MIN_HEAD_ANGLE.radians)
    time.sleep(1)

    cli.set_lift_height(pycozmo.MAX_LIFT_HEIGHT.mm)
    time.sleep(1)
    cli.set_lift_height(pycozmo.MIN_LIFT_HEIGHT.mm)
    time.sleep(1)


pycozmo.run_program(pycozmo_program)
