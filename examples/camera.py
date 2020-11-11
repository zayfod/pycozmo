#!/usr/bin/env python

import time

import pycozmo


def on_camera_image(cli, image):
    image.save("camera.png", "PNG")


with pycozmo.connect() as cli:

    # Raise head.
    angle = (pycozmo.robot.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians) / 2.0
    cli.set_head_angle(angle)

    cli.enable_camera(enable=True, color=True)

    # Wait for image to stabilize.
    time.sleep(2.0)

    cli.add_handler(pycozmo.event.EvtNewRawCameraImage, on_camera_image, one_shot=True)

    # Wait for image to be captured.
    time.sleep(1)
