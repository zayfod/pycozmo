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

    # List of face expressions.
    expressions = [
        pycozmo.expressions.Anger(),
        pycozmo.expressions.Sadness(),
        pycozmo.expressions.Happiness(),
        pycozmo.expressions.Surprise(),
        pycozmo.expressions.Disgust(),
        pycozmo.expressions.Fear(),
        pycozmo.expressions.Pleading(),
        pycozmo.expressions.Vulnerability(),
        pycozmo.expressions.Despair(),
        pycozmo.expressions.Guilt(),
        pycozmo.expressions.Disappointment(),
        pycozmo.expressions.Embarrassment(),
        pycozmo.expressions.Horror(),
        pycozmo.expressions.Skepticism(),
        pycozmo.expressions.Annoyance(),
        pycozmo.expressions.Fury(),
        pycozmo.expressions.Suspicion(),
        pycozmo.expressions.Rejection(),
        pycozmo.expressions.Boredom(),
        pycozmo.expressions.Tiredness(),
        pycozmo.expressions.Asleep(),
        pycozmo.expressions.Confusion(),
        pycozmo.expressions.Amazement(),
        pycozmo.expressions.Excitement(),
    ]

    # Base face expression.
    base_face = pycozmo.expressions.Neutral()

    rate = pycozmo.robot.FRAME_RATE
    timer = pycozmo.util.FPSTimer(rate)
    for expression in expressions:

        # Transition from base face to expression and back.
        for from_face, to_face in ((base_face, expression), (expression, base_face)):

            if to_face != base_face:
                print(to_face.__class__.__name__)

            # Generate transition frames.
            face_generator = pycozmo.procedural_face.interpolate(from_face, to_face, rate // 3)
            for face in face_generator:

                # Render face image.
                im = face.render()

                # The Cozmo protocol expects a 128x32 image, so take only the even lines.
                np_im = np.array(im)
                np_im2 = np_im[::2]
                im2 = Image.fromarray(np_im2)

                # Display face image.
                cli.display_image(im2)

                # Maintain frame rate.
                timer.sleep()

            # Pause for 1s.
            for i in range(rate):
                timer.sleep()
