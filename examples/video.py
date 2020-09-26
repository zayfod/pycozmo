#!/usr/bin/env python

import time

import pycozmo


# Last image, received from the robot.
last_im = None


def on_camera_image(cli, new_im):
    """ Handle new images, coming from the robot. """
    del cli

    global last_im
    last_im = new_im


def pycozmo_program(cli: pycozmo.client.Client):

    global last_im

    # Raise head.
    angle = (pycozmo.robot.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians) / 2.0
    cli.set_head_angle(angle)

    # Register to receive new camera images.
    cli.add_handler(pycozmo.event.EvtNewRawCameraImage, on_camera_image)

    # Enable camera.
    pkt = pycozmo.protocol_encoder.EnableCamera()
    cli.conn.send(pkt)

    while True:

        if last_im:

            # Get last image.
            im = last_im

            # Resize from 320x240 to 128x32.
            im = im.resize((128, 32))
            # Convert to binary image.
            im = im.convert('1')

            # Display the result image.
            cli.display_image(im)

        # Run with 25 FPS.
        time.sleep(1 / 25)


pycozmo.run_program(pycozmo_program, protocol_log_level="INFO", robot_log_level="DEBUG")
