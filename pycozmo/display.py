#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2 as cv


class Display(object):
    """
    This is just a wrapper around the imshow() method from the OpenCV library to make things more convenient.
    """

    def __init__(self, win_name):
        """
        Initialize the parameters required for displaying images.
        :param win_name: String. The name of the window in which the video stream will be displayed.
        """

        # Call the constructor for the parent class
        super(Display, self).__init__()

        # Store the name of the window
        self._win_name = win_name

        # Initialize a display thread
        cv.startWindowThread()
        # And a named window inside it
        cv.namedWindow(self._win_name)

    def step(self, frame):
        """
        Take the frame give in parameter and display it in the window.
        :param frame: Numpy.ndarray. A numpy array representing the next frame in the video stream.
        :return: None
        """

        # Do what it says on the tin
        cv.imshow(self._win_name, frame)

    def stop(self):
        """
        Destroy the named window created upon initialization.
        :return: None
        """

        # Do what it says on the tin
        cv.destroyWindow(self._win_name)
