#!/usr/bin/env python

import time

import pycozmo


with pycozmo.connect() as cli:

    while True:
        time.sleep(0.1)
