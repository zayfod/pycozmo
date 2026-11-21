#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
from queue import Queue, Empty
import logging
import numpy as np
import cv2 as cv
import pycozmo as pc

# Set that to False if you want Cozmo's camera to return grayscale images
COLOR_IMG = True

# Define the increments for the linear and angular velocities, as well as the
# head angle and lift height
LIN_INC = 20
ANG_INC = math.radians(20)
HEAD_INC = math.radians(2)
LIFT_INC = 5

# This is required since Open CV cannot open displays from threads.
IMG_QUEUE = Queue()

# The linear velocity is expressed in mm/s and the angular velocity in rad/s
LIN_VELOCITY = 0
ANG_VELOCITY = 0
HEAD_TILT = (pc.MAX_HEAD_ANGLE.radians - pc.MIN_HEAD_ANGLE.radians) * 0.1
HEAD_LIGHT = False
LIFT_HEIGHT = pc.MIN_LIFT_HEIGHT.mm

# Those parameters are used to configure the unsharp masking algorithm
# Play with them to get the best image you can
SHARP_AMOUNT = 0.7
SHARP_GAMMA = 2.2


# NOTE: This could be used with cv.filter2D() in place of the unsharp masking
# However, controlling the amount of sharpening is more difficult
# UNSHARP_KERNEL = -1 / 256 * np.array([[1, 4, 6, 4, 1],
#                                       [4, 16, 24, 16, 4],
#                                       [6, 24, -476, 24, 6],
#                                       [4, 16, 24, 16, 4],
#                                       [1, 4, 6, 4, 1]])


def on_camera_img(cli, image):
    """
    A simple function that converts a frame from Cozmo's camera into a BGR
    formatted image to be used by OpenCV.
    :param cli: An instance of the pycozmo.Client class representing the robot.
    :param image: A color/grayscale frame from Cozmo's camera.
    :return: None
    """
    global IMG_QUEUE

    # Convert the image into a numpy array so that OpenCV can manipulate it
    orig_img = np.array(image)

    # Check if we got a color image
    if orig_img.shape[-1] == 3:
        # The thing about OpenCV is that it uses BGR formatted images for
        # reasons
        orig_img = cv.cvtColor(orig_img, cv.COLOR_RGB2BGR)

    # Resize the image
    # The lanczos4 algorithm produces the best results, but might be slow
    # you can use cv.INTER_LINEAR for poorer, but faster results
    resized_img = cv.resize(orig_img, None, fx=2, fy=2,
                            interpolation=cv.INTER_LANCZOS4)

    # Try to reduce the noise using unsharp masking
    # An explanation for this technique can be found here:
    # https://en.wikipedia.org/wiki/Unsharp_masking#Digital_unsharp_masking
    blurred_img = cv.GaussianBlur(resized_img, (3, 3), 0)
    sharp_img = cv.addWeighted(resized_img, 1 + SHARP_AMOUNT, blurred_img,
                               -SHARP_AMOUNT, gamma=SHARP_GAMMA)

    # Send the image back to the main thread for display
    IMG_QUEUE.put(sharp_img)


def stop_all(cli, state):
    """
    This function simply stops all motors and resets the corresponding
    velocities. It is used when Cozmo detects that it has been picked up, or is
    about to fall off a cliff.
    :param cli: An instance of the pycozmo.Client class representing the robot.
    :param state: A boolean set to True if Cozmo has been picked up or is about
    to fall off a cliff. False otherwise.
    :return: None
    """
    global LIN_VELOCITY, ANG_VELOCITY

    # Well as said above, if Cozmo is not touching the ground anymore we stop
    # all motors to prevent any damage
    if state:
        # Stop the motors
        cli.stop_all_motors()

        # Reset the linear and angular velocities
        LIN_VELOCITY = 0
        ANG_VELOCITY = 0


if __name__ == "__main__":
    # Connect to the robot
    with pc.connect() as cli:
        try:
            # Look forward
            cli.set_head_angle(HEAD_TILT)

            # Enable the camera
            cli.enable_camera(enable=True, color=COLOR_IMG)

            # Set the lift in its minimum position
            cli.set_lift_height(height=LIFT_HEIGHT)

            # Handle new incoming images
            cli.add_handler(pc.event.EvtNewRawCameraImage, on_camera_img)

            # Handle cliff and pick-up detection
            cli.add_handler(pc.event.EvtCliffDetectedChange, stop_all)
            cli.add_handler(pc.event.EvtRobotPickedUpChange, stop_all)

            # Loop forever
            while True:
                try:
                    # Get the next frame from the camera
                    # A timeout is applied so that the robot might still be
                    # controlled even if no image can be displayed
                    img = IMG_QUEUE.get(timeout=0.2)
                    # Display the frame in a window
                    cv.imshow('Camera', img)
                    IMG_QUEUE.task_done()
                except Empty:
                    logging.warning('Did not get any image from the camera so '
                                    'not displaying any.')

                # Read the next key event
                # /!\ It should be noted that that if OpenCV's window displaying
                # the image received from the camera loses focus, then Cozmo
                # will not answer your commands anymore.
                key = cv.waitKeyEx(1)

                # Act accordingly
                if key == ord('q'):
                    # Exit the program
                    break

                # Losing a bit of computational time to prevent sending motor
                # commands on each loop even when not necessary
                if key in [ord('w'), ord('s'), ord('a'), ord('d')]:
                    if key == ord('w'):
                        print('up')
                        # Increase the linear velocity
                        LIN_VELOCITY = min(pc.MAX_WHEEL_SPEED.mmps,
                                           LIN_VELOCITY + LIN_INC)
                    elif key == ord('s'):
                        # Decrease the linear velocity
                        LIN_VELOCITY = max(-pc.MAX_WHEEL_SPEED.mmps,
                                           LIN_VELOCITY - LIN_INC)
                    elif key == ord('a'):
                        # Increase the angular velocity
                        ANG_VELOCITY = min(pc.MAX_WHEEL_SPEED.mmps / pc.TRACK_WIDTH.mm,
                                           ANG_VELOCITY + ANG_INC)
                    elif key == ord('d'):
                        # Decrease the angular velocity
                        ANG_VELOCITY = max(-pc.MAX_WHEEL_SPEED.mmps / pc.TRACK_WIDTH.mm,
                                           ANG_VELOCITY - ANG_INC)

                    # Compute the velocity of the left and right wheels
                    # using the inverse kinematic equations for a differential
                    # drive robot
                    l_speed = min(pc.MAX_WHEEL_SPEED.mmps,
                                  LIN_VELOCITY - (
                                          pc.TRACK_WIDTH.mm * ANG_VELOCITY) / 2)
                    r_speed = min(pc.MAX_WHEEL_SPEED.mmps,
                                  LIN_VELOCITY + (
                                          pc.TRACK_WIDTH.mm * ANG_VELOCITY) / 2)

                    # Send the command to the robot
                    cli.drive_wheels(lwheel_speed=l_speed,
                                     rwheel_speed=r_speed)

                # Same as above, sacrificing a bit of computational time to
                # prevent sending extraneous head tilt commands
                elif key in [ord('k'), ord('j')]:
                    if key == ord('k'):
                        # Increase head tilt
                        HEAD_TILT = min(pc.MAX_HEAD_ANGLE.radians,
                                        HEAD_TILT + HEAD_INC)
                    elif key == ord('j'):
                        # Decrease head tilt
                        HEAD_TILT = max(pc.MIN_HEAD_ANGLE.radians,
                                        HEAD_TILT - HEAD_INC)

                    # Set the head angle
                    cli.set_head_angle(HEAD_TILT)

                # You get the idea by now
                elif key in [ord('n'), ord('m')]:
                    if key == ord('m'):
                        # Increase the lift height
                        LIFT_HEIGHT = min(pc.MAX_LIFT_HEIGHT.mm,
                                          LIFT_HEIGHT + LIFT_INC)
                    elif key == ord('n'):
                        # Decrease lift height
                        LIFT_HEIGHT = max(pc.MIN_LIFT_HEIGHT.mm,
                                          LIFT_HEIGHT - LIFT_INC)

                    # Set the height of the lift
                    cli.set_lift_height(height=LIFT_HEIGHT)
                elif key == ord('l'):
                    # Toggle the head light
                    HEAD_LIGHT = not HEAD_LIGHT
                    # Set the head light
                    cli.set_head_light(enable=HEAD_LIGHT)

                else:
                    # Other keys have no effect, so skip the rest
                    continue

                print("Velocities: {:.2f} mm/s, {:.2f} deg/s, "
                      "Head angle: {:.2f} deg, "
                      "Head Light enabled: {}".format(LIN_VELOCITY,
                                                      math.degrees(ANG_VELOCITY),
                                                      math.degrees(HEAD_TILT),
                                                      HEAD_LIGHT), end='\r')
        finally:
            # This is to make sure that whatever happens during execution, the
            # robot will always stop driving before exiting
            cli.stop_all_motors()

            # Bring the lift down
            cli.set_lift_height(height=pc.MIN_LIFT_HEIGHT.mm)

            # Set the head down as well
            cli.set_head_angle(pc.MIN_HEAD_ANGLE.radians)

            # Close any display open by OpenCv
            cv.destroyAllWindows()

            # Make sure the queue is empty, even if this has no real impact
            while not IMG_QUEUE.empty():
                IMG_QUEUE.get()
                IMG_QUEUE.task_done()
            IMG_QUEUE.join()
