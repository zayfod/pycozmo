#!/usr/bin/env python

from PIL import Image
import pycozmo


# Last image, received from the robot.
last_im = None


def on_camera_image(cli, new_im):
    """ Handle new images, coming from the robot. """
    global last_im
    last_im = new_im


with pycozmo.connect(enable_procedural_face=False) as cli:

    # Raise head.
    angle = (pycozmo.robot.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians) / 2.0
    cli.set_head_angle(angle)

    # Register to receive new camera images.
    cli.add_handler(pycozmo.event.EvtNewRawCameraImage, on_camera_image)

    # Enable camera.
    cli.enable_camera()

    # Run with 14 FPS. This is the frame rate of the robot camera.
    timer = pycozmo.util.FPSTimer(14)
    while True:

        if last_im:

            # Get last image.
            im = last_im

            # Resize from 320x240 to 68x17. Larger image sometime are too big for the robot receive buffer.
            im = im.resize((68, 17))
            # Convert to binary image.
            im = im.convert('1')
            # Mirror the image.
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
            # Construct a 128x32 image that the robot can display.
            im2 = Image.new("1", (128, 32))
            im2.paste(im, (30, 7))
            # Display the result image.
            cli.display_image(im2)

        timer.sleep()
