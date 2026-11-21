#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import path
from enum import IntEnum
from threading import Thread
from collections import deque
import numpy as np
import cv2 as cv


# TODO: Replace this monstrosity with util.get_cozmo_asset_dir()
#       or util.get_cozmo_dir(), depending on where the weights
#       and such configuration should live.
BASE_DIR = path.abspath(path.dirname(__file__))


class ObjCat(IntEnum):
    HAND = 0
    HEAD = 1


class ObjectDetector(Thread):
    """
    A class that uses a Yolo V4 neural network to detect objects of different categories in a frame.
    """

    def __init__(self, obj_cats, conf_thres=0.5, nms_thres=0.3, img_w=704, img_h=704,
                 classes_name_file=path.join(BASE_DIR, 'trackerCfg', 'openimages.names'),
                 model_conf_file=path.join(BASE_DIR, 'trackerCfg', 'yolo.cfg'),
                 model_weight_file=path.join(BASE_DIR, 'trackerCfg', 'yolo.weights')):
        """
        Initialize the different attributes required to detect objects in pictures.
        :param obj_cats: List. A list of categories of objects to detect and track in every picture.
        :param conf_thres: Float. The confidence threshold above which an object is considered as detected.
        :param nms_thres: Float. The non-maximum threshold which determines how dissimilar two objects should be to be
        considered as separate.
        :param img_w: Int. The width of the frame passed to the detector network. This size should be a multiple of 32.
        :param img_h: Int. The height of the frame passed to the detector network. This size should be a multiple of 32.
        :param classes_name_file: String. The relative path to the text file containing the name of the categories of
        object to be detected.
        :param model_conf_file: String. The relative path to the file containing the configuration of the YoloV4 network
        to be used as the object detector.
        :param model_weight_file: String. The relative path to the file containing the pre-trained weights for the
        detector network.
        """

        # Call the constructor for the parent class
        super(ObjectDetector, self).__init__()

        # Classes and categories management
        assert hasattr(obj_cats, '__getitem__')
        self._tracked_cats = obj_cats
        self._avail_classes = []
        with open(classes_name_file, 'rt') as f:
            self._avail_classes = f.read().rstrip('\n').split('\n')

        # Yolo parameters
        self._conf_thres = conf_thres
        self._nms_thres = nms_thres
        self._img_size = (img_w, img_h)

        # Instantiate a yolo-based object detection network
        self._dnn = cv.dnn.readNetFromDarknet(model_conf_file,
                                              model_weight_file)
        self._dnn.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
        self._dnn.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)
        # Get the name of the output layers
        self._out_layers_name = [self._dnn.getLayerNames()[i[0] - 1] for i in
                                 self._dnn.getUnconnectedOutLayers()]

        # Initialize a deque in which the next frame to be processed will be put
        # We limit the size of the deque to 1 since only the most recent frame is of interest to us
        self._in_queue = deque(maxlen=1)

        # Initialize a list of callable observers to notify when detecting objects
        self._observers = []

        # Define a flag telling the thread when to stop
        self._continue = True

    def add_listener(self, func):
        """
        Add a function to the list of observers for the availability of new bounding boxes.
        :param func: Callable. A callable that takes a dictionary of bounding boxes, and a frame
        as parameters.
        :return: None
        """

        # Make sure the given parameter is a callable
        if callable(func):
            # Add the listener to the list
            self._observers.append(func)
        else:
            print('The parameter {} provided should be a callable.'.format(func))

    def remove_listener(self, func):
        """
        Remove a function from the list of observers.
        :param func: Callable. A function previously added to the list of observers.
        :return: None
        """

        try:
            # Remove the corresponding listener from the list of observers
            self._observers.remove(func)
        except ValueError:
            print('{} was not found in the list of observers, so not removed.'.format(func))

    def clear_listeners(self):
        """
        Remove all the observers.
        :return: None
        """

        # Assign a new empty list to the observers attribute
        self._observers = []

    def run(self):
        while self._continue:
            try:
                # Get the next frame
                frame = self._in_queue.pop()
            except IndexError:
                continue

            # Detect objects and extract corresponding bboxes
            outs = self._detect(frame)
            frame_h, frame_w = frame.shape[0:2]
            bboxes = self._extract_bboxes(outs, frame_w, frame_h)

            # Make sure the thread was not killed during processing
            if self._continue and len(bboxes) != 0:
                # Notify the listeners of the new bounding boxes
                for obs in self._observers:
                    obs(bboxes, frame)

    def stop(self):
        """
        Cleanup before destroying the instance.
        :return: None
        """

        # Ask the thread to stop
        self._continue = False

        # Empty the input queue
        print('D: Emptying input queue ...')
        self._in_queue.clear()
        print('D: Done.')

    def detect_objects(self, frame):
        """
        A simple wrapper around the append() method of the detector's input deque.
        Therefore, it just adds the frame given in parameter to the deque.
        :param frame: Numpy.ndarray. An array representing a frame from the video stream, in which
        objects are to be detected.
        :return: None
        """

        # Add the given frame to the input queue so that it is processed during the next cycle
        self._in_queue.append(frame)

    def _detect(self, frame):
        # Create a blob from the image
        blob = cv.dnn.blobFromImage(frame, 1 / 255, (self._img_size[0],
                                                     self._img_size[1]),
                                    [0, 0, 0], 1, crop=False)

        # Set the blob as the network's input
        self._dnn.setInput(blob)

        # Run the forward pass to get a prediction
        return self._dnn.forward(self._out_layers_name)

    def _extract_bboxes(self, outs, frame_w, frame_h):
        # TODO: Add comment to describe what you are doing here
        outs = np.vstack(outs)
        confidences = np.max(outs[:, 5:], axis=1)
        outs = outs[np.flatnonzero(confidences > self._conf_thres), :]
        if outs.size == 0:
            return {}

        # Compute the centers and the size of the bounding boxes
        # center_x, center_y, width, height all relative to frame size
        outs[:, 0:4] *= np.array([frame_w, frame_h, frame_w, frame_h])
        center = outs[:, 0:2]
        size = outs[:, 2:4]
        left_top = center - size/2
        boxes = np.hstack((left_top, size)).astype(np.intp).tolist()

        # Non Maximum suppression
        confidences = np.max(outs[:, 5:], axis=-1)
        indices = cv.dnn.NMSBoxes(boxes, confidences, self._conf_thres,
                                  self._nms_thres)
        bboxes = {}
        class_ids = np.argmax(outs[:, 5:], axis=-1)
        for i in indices.flatten():
            cat = ObjCat(class_ids[i])
            if cat in self._tracked_cats:
                bboxes.setdefault(cat, []).append((boxes[i], confidences[i]))
        return bboxes
