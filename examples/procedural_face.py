#!/usr/bin/env python

import time

from PIL import Image
import numpy as np

import pycozmo


with pycozmo.connect(enable_procedural_face=False) as cli:

    # Raise head.
    angle = (pycozmo.robot.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians) / 2.0
    cli.set_head_angle(angle)
    time.sleep(1)

    # Render a 128x64 procedural face with default parameters.
    f = pycozmo.procedural_face.ProceduralFace()
    im = f.render()

    # The Cozmo protocol expects a 128x32 image, so take only the even lines.
    np_im = np.array(im)
    np_im2 = np_im[::2]
    im2 = Image.fromarray(np_im2)

    cli.display_image(im2, 5.0)
