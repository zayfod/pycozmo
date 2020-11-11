#!/usr/bin/env python

import os
import time

from PIL import Image

import pycozmo


with pycozmo.connect() as cli:

    # Raise head.
    angle = (pycozmo.robot.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians) / 2.0
    cli.set_head_angle(angle)
    time.sleep(1)

    # Load image
    im = Image.open(os.path.join(os.path.dirname(__file__), "..", "assets", "pycozmo.png"))
    # Convert to binary image.
    im = im.convert('1')

    cli.display_image(im, 5.0)
