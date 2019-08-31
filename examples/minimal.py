#!/usr/bin/env python

import time

import pycozmo


def pycozmo_program(cli):
    while True:
        time.sleep(0.1)


pycozmo.run_program(pycozmo_program)
