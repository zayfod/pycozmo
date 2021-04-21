#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from enum import IntEnum, auto
from queue import Queue, Empty
import numpy as np
import cv2 as cv
import pycozmo as pc
from pynput import keyboard as kbd


# Declare an enumeration providing all the directions in which Cozmo can move
class Direction(IntEnum):
    NONE = auto()
    FORWARD = auto()
    BACKWARD = auto()
    LEFT = auto()
    RIGHT = auto()


# Declare a flag telling the program's main loop to stop
GO_ON = True


class OpencvRC(object):
    """
    A remote controller using OpenCV's GUI to display Cozmo's video feed, as
    well as set its velocities, head angle, and lift height. Movement and head
    light are controlled using the keyboard (W, A, S, D, and L).
    """

    def __init__(self, win_name='Control Panel', sharp_amount=0.7,
                 sharp_gamma=2.2):
        """
        Initialize all the variables required to remote control Cozmo using
        OpenCV's GUI and Pynput for handling keyboard events.
        :param win_name: String. The title of the window in which OpenCV will
        display the camera feed, as well as the different taskbars.
        :param sharp_amount: Float. Used in the unsharp masking algorithm to
        dictate how much of the blurred image gets added to scaled image.
        :param sharp_gamma: Float. A scalar added during the summing process in
        the unsharp masking algorithm, to effectively brighten or darken the
        overall image.
        """

        # Should the camera image be displayed in color or grayscale
        self._color = True

        # Keep track of Cozmo's current action
        self._action = {'linear': Direction.NONE, 'angular': Direction.NONE}

        # Keep track of Cozmo's linear and angular velocities
        self._velocity = {'linear': 0, 'angular': 0}

        # Keep track of the head light state
        self._head_light = False

        # Keep track of the head tilt angle
        self._head_tilt = pc.MIN_HEAD_ANGLE.radians

        # Keep track of the lift's height
        self._lift_height = pc.MIN_LIFT_HEIGHT.mm

        # Initialize Cozmo's client
        self._cozmo_clt = pc.Client()

        # Initialize a listener to monitor keyboard events
        self._kbd_listener = kbd.Listener(on_press=self._on_keypress,
                                          on_release=self._on_keyrelease)

        # Initialize a queue to pass images between the thread receiving them
        # and the main loop
        self._image_queue = Queue()

        # Other miscellaneous parameters to keep track of
        self._win_name = win_name
        self._sharp_amount = sharp_amount
        self._sharp_gamma = sharp_gamma

    def init(self):
        """
        Create the window OpenCV will use to display the video feed and the
        different trackbars, as well as set and start Cozmo's client, and the
        keyboard listener.
        :return: None
        """

        # Create a window for the control panel
        cv.namedWindow(self._win_name)

        # Create the different trackbars controlling the robot's velocities,
        # head tilt, and lift height
        cv.createTrackbar('Linear Velocity', self._win_name, 0, 100,
                          self._on_linear_velocity_change)
        cv.createTrackbar('Angular Velocity', self._win_name, 0, 100,
                          self._on_angular_velocity_change)
        cv.createTrackbar('Head tilt', self._win_name, 0, 100,
                          self._on_head_tilt_change)
        cv.createTrackbar('Lift height', self._win_name, 0, 100,
                          self._on_lift_height_change)

        # Start Cozmo's client and connect to the robot
        self._cozmo_clt.start()
        self._cozmo_clt.connect()
        self._cozmo_clt.wait_for_robot()

        # Set Cozmo in its initial state
        # Look down
        self.head_tilt = pc.MIN_HEAD_ANGLE.radians

        # Set the lift in its minimum position
        self.lift_height = pc.MIN_LIFT_HEIGHT.mm

        # Make sure the light is off by default
        self.head_light = False

        # Enable the camera
        self._cozmo_clt.enable_camera(enable=True, color=self._color)

        # Handle new incoming images
        self._cozmo_clt.add_handler(pc.event.EvtNewRawCameraImage,
                                    self._on_new_image)

        # Handle cliff and pick-up detection
        self._cozmo_clt.add_handler(pc.event.EvtCliffDetectedChange,
                                    self._stop_all)
        self._cozmo_clt.add_handler(pc.event.EvtRobotPickedUpChange,
                                    self._stop_all)

        # Start the keyboard event listener
        self._kbd_listener.start()
        self._kbd_listener.wait()

    def step(self):
        """
        Get the next frame from the queue and have OpenCV display it in a
        window.
        :return: None
        """

        try:
            # Get the next frame from the queue
            img = self._image_queue.get(timeout=0.2)
            # Display the frame in a window
            cv.imshow(self._win_name, img)
            self._image_queue.task_done()
        except Empty:
            logging.warning("Did not get any image from the robot.")

        # This looks stupid, but is required by OpenCV to actually draw
        # the image on the window.
        # See OpenCV's documentation on imshow for a more "in depth"
        # explanation
        cv.waitKey(25)

    def stop(self):
        """
        Clean up after execution to leave the program in a known and stable
        state (hopefully).
        :return: None
        """

        # This is to make sure that whatever happens during execution, the
        # robot will always stop driving before exiting
        self._stop_all()

        # Bring the lift down
        self.lift_height = pc.MIN_LIFT_HEIGHT.mm

        # Set the head down as well
        self.head_tilt = pc.MIN_HEAD_ANGLE.radians

        # Turn off the light
        self.head_light = False

        # Disconnect from Cozmo
        self._cozmo_clt.disconnect()
        self._cozmo_clt.stop()

        # If the keyboard listener is still running
        if self._kbd_listener.running:
            self._kbd_listener.stop()
            self._kbd_listener.join()

        # Close any display open by OpenCv
        cv.destroyAllWindows()

        # Make sure the image queue is empty, even if this has no real impact
        while not self._image_queue.empty():
            self._image_queue.get()
            self._image_queue.task_done()
        self._image_queue.join()

    def _on_new_image(self, cli, frame):
        """
        A simple function that converts a frame from Cozmo's camera into a
        up-scaled and BGR formatted image to be used by OpenCV.
        :param cli: An instance of the pycozmo. Client class representing the
        robot.
        :param frame: A color/grayscale frame from Cozmo's camera.
        :return: None
        """

        # Convert the image into a numpy array so that OpenCV can manipulate it
        orig_img = np.array(frame)

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
        sharp_img = cv.addWeighted(resized_img, 1 + self._sharp_amount,
                                   blurred_img, -self._sharp_amount,
                                   gamma=self._sharp_gamma)

        # NOTE: This could be used with cv.filter2D() in place of the unsharp
        # masking. However, controlling the amount of sharpening is more
        # difficult
        # UNSHARP_KERNEL = -1 / 256 * np.array([[1, 4, 6, 4, 1],
        #                                       [4, 16, 24, 16, 4],
        #                                       [6, 24, -476, 24, 6],
        #                                       [4, 16, 24, 16, 4],
        #                                       [1, 4, 6, 4, 1]])

        # Send the image back to the main thread for display
        self._image_queue.put(sharp_img)

    def _set_action(self, linear, angular):
        """
        Set the directions of Cozmo's movement and send the corresponding
        command to spin the motors at the right speed.
        :param linear: Direction. An instance of the Direction enumeration.
        Either Forward, Backward, or None.
        :param angular: Direction. An instance of the Direction enumeration.
        Either Left, Right, or None.
        :return: None
        """

        # Check if the new values are different from the old ones before doing
        # any complex calculations and send motor commands
        if self._action['linear'] != linear or \
                self._action['angular'] != angular:

            # Set the value of the new action
            self._action['linear'] = linear
            self._action['angular'] = angular

            # If Cozmo is not doing anything, simply stop all the motors
            if self._action['linear'] == Direction.NONE and \
                    self._action['angular'] == Direction.NONE:
                self._cozmo_clt.stop_all_motors()

            # Compute the speed of each wheel depending on Cozmo's action and
            # the new values for the linear and angular velocities
            else:
                # Are we going forward, backward, or not moving in this
                # direction at all?
                if self._action['linear'] == Direction.FORWARD:
                    lin_vel = self._velocity['linear']
                elif self._action['linear'] == Direction.BACKWARD:
                    lin_vel = -self._velocity['linear']
                else:
                    lin_vel = 0

                # Are we going left, right, or not moving in this direction at
                # all?
                if self._action['angular'] == Direction.LEFT:
                    ang_vel = self._velocity['angular']
                elif self._action['angular'] == Direction.RIGHT:
                    ang_vel = -self._velocity['angular']
                else:
                    ang_vel = 0

                # Compute the actual speed of each wheel
                left = min(pc.MAX_WHEEL_SPEED.mmps, lin_vel -
                           (pc.TRACK_WIDTH.mm * ang_vel) / 2)
                right = min(pc.MAX_WHEEL_SPEED.mmps, lin_vel +
                            (pc.TRACK_WIDTH.mm * ang_vel) / 2)

                # Send the command to the motors
                self._cozmo_clt.drive_wheels(lwheel_speed=left,
                                             rwheel_speed=right)

    def _stop_all(self, *args):
        """
        Simply stop all motors and set both linear and angular actions to NONE.
        This is a wrapper for ease of use as a callback.
        :return: None
        """

        # Set both actions to NONE, which will stop the motors
        self._set_action(Direction.NONE, Direction.NONE)

    def _on_head_tilt_change(self, value):
        """
        Simply change the head tilt based on the value given in parameter.
        :param value: Float. A value between 0: head fully down,
        and 100: head fully up.
        :return: None
        """

        # Transform the value into a percentage
        value /= 100

        # Set the new head tilt based on the value in parameter
        self.head_tilt = value * pc.MAX_HEAD_ANGLE.radians + \
                         (1 - value) * pc.MIN_HEAD_ANGLE.radians

    def _on_lift_height_change(self, value):
        """
        Simply update the height of Cozmo's lift based on the value given in
        parameter.
        :param value: Float. A value between 0: lift fully down,
        and 100: lift fully up.
        :return: None
        """

        # Transform the value into a percentage
        value /= 100

        # Set the new lift's height based on the value in parameter
        self.lift_height = value * pc.MAX_LIFT_HEIGHT.mm + \
                           (1 - value) * pc.MIN_LIFT_HEIGHT.mm

    def _on_linear_velocity_change(self, value):
        """
        Simply update Cozmo's linear velocity based on the value given in
        parameter.
        :param value: Float. A value between 0: Stopped, and 100: Full speed
        ahead.
        :return: None
        """

        # Set the new linear velocity
        self.linear_velocity = pc.MAX_WHEEL_SPEED.mmps * value / 100

    def _on_angular_velocity_change(self, value):
        """
        Simply update Cozmo's angular velocity based on the value given in
        parameter.
        :param value: Float. A value between 0: Stopped, and
        100: I gonna throw-up-make-it-stop.
        :return: None
        """

        # Set the new angular velocity
        self.angular_velocity = (pc.MAX_WHEEL_SPEED.mmps / pc.TRACK_WIDTH.mm) \
                                * value / 100

    def _on_keypress(self, key):
        """
        A callback handling keypress events. More specifically it is used to
        exit the program, and control the robot's movements.
        :param key: An instance of pynput.keyboard.Key, pynput.keyboard.KeyCode
        or None. The Key class represent special keys, such as esc, alt, and so
        on. The KeyCode class on the other hand is a simple wrapper converting
        keycodes into characters.
        :return: None
        """
        global GO_ON

        # Ignore any None or pynput.keyboard.Key instances
        if key is not None and not isinstance(key, kbd.Key):

            # Get the character corresponding to the pressed key
            char = key.char

            if char == 'q':
                # Tell the main loop to stop
                GO_ON = False

            if (char in ['w', 's'] and
                self._action['linear'] == Direction.NONE) or \
                    (char in ['a', 'd'] and
                     self._action['angular'] == Direction.NONE):

                # Initialize the new action
                linear, angular = self._action.values()

                # Move forward
                if char == 'w':
                    linear = Direction.FORWARD

                # Move backward
                elif char == 's':
                    linear = Direction.BACKWARD

                # Turn left
                elif char == 'a':
                    angular = Direction.LEFT

                # Turn right
                elif char == 'd':
                    angular = Direction.RIGHT

                # Set the new actions
                self._set_action(linear, angular)

            elif char == 'l':
                # Toggle the head light
                self.head_light = not self.head_light

    def _on_keyrelease(self, key):
        """
        A callback handling keyrelease events. More specifically it is used to
        control the robot's movements.
        :param key: An instance of pynput.keyboard.Key, pynput.keyboard.KeyCode
        or None. The Key class represent special keys, such as esc, alt, and so on.
        The KeyCode class on the other hand is a simple wrapper converting keycodes
        into characters.
        :return: None
        """
        global GO_ON

        # Ignore any event if the program is in the process of exiting
        if GO_ON:
            # Ignore any None or pynput.keyboard.Key instances
            if key is not None and not isinstance(key, kbd.Key):
                # Get the character corresponding to the released key
                char = key.char

                # Initialize the new action
                linear, angular = self._action.values()

                # Stop moving forward
                if char == 'w' and self._action['linear'] == Direction.FORWARD:
                    linear = Direction.NONE

                # Stop moving backward
                if char == 's' and self._action['linear'] == Direction.BACKWARD:
                    linear = Direction.NONE

                # Stop turning left
                if char == 'a' and self._action['angular'] == Direction.LEFT:
                    angular = Direction.NONE

                # Stop turning right
                if char == 'd' and self._action['angular'] == Direction.RIGHT:
                    angular = Direction.NONE

                # Set the new actions
                self._set_action(linear, angular)

    @property
    def head_light(self):
        return self._head_light

    @head_light.setter
    def head_light(self, value):
        """
        Toggle the state of the light.
        :param value: Bool. True for turning the light on, False otherwise.
        :return: None
        """

        if self._head_light != value:
            # Set the value
            self._head_light = value

            # Tell Cozmo to actually turn the light on/off
            self._cozmo_clt.set_head_light(enable=self._head_light)

    @property
    def head_tilt(self):
        return self._head_tilt

    @head_tilt.setter
    def head_tilt(self, value):
        """
        Set the head tilt and tell Cozmo to actually move its head.
        :param value: Float. The new head angle in radians.
        :return: None
        """

        # Set the value of the head tilt
        self._head_tilt = max(pc.MIN_HEAD_ANGLE.radians,
                              min(pc.MAX_HEAD_ANGLE.radians, value))

        # Send the command to cozmo
        self._cozmo_clt.set_head_angle(self._head_tilt)

    @property
    def lift_height(self):
        return self._lift_height

    @lift_height.setter
    def lift_height(self, value):
        """
        Set the lift height and tell Cozmo to actually move the lift.
        :param value: Float. The new horizontal position of the lift in mm.
        :return: None
        """

        # Set the value of the lift height
        self._lift_height = max(pc.MIN_LIFT_HEIGHT.mm,
                                min(pc.MAX_LIFT_HEIGHT.mm, value))

        # Send the command to cozmo
        self._cozmo_clt.set_lift_height(height=self._lift_height)

    @property
    def linear_velocity(self):
        return self._velocity['linear']

    @linear_velocity.setter
    def linear_velocity(self, value):
        self._velocity['linear'] = max(0, min(value, pc.MAX_WHEEL_SPEED.mmps))

    @property
    def angular_velocity(self):
        return self._velocity['angular']

    @angular_velocity.setter
    def angular_velocity(self, value):
        self._velocity['angular'] = max(0, min(value,
                                        pc.MAX_WHEEL_SPEED.mmps / pc.TRACK_WIDTH.mm))

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        """
        Switch between colored and grayscale image for Cozmo's video feed.
        :param value: Bool. True displays a colored image, a grayscale one
        otherwise.
        :return: None
        """

        if self._color != value:
            # Set the new value for the color switch
            self._color = value

            # Tell cozmo to actually change the image
            self._cozmo_clt.enable_camera(enable=True, color=value)


if __name__ == "__main__":
    # Instantiate a new remote controller
    rc = OpencvRC()

    # Initialize the remote controller
    rc.init()

    try:
        # Loop until told to stop
        while GO_ON:

            # Execute the next step
            rc.step()

    finally:
        # Stop the remote controller and clean after ourselves
        rc.stop()
