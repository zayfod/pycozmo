#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from queue import Queue, Empty
from threading import Thread
from enum import IntEnum
from itertools import chain
from random import randint
import cv2 as cv


class TrackType(IntEnum):
    CSRT = 0
    KCF = 1
    MOSSE = 2


class ObjectTracker(Thread):
    """
    A class that uses multiple trackers to follow detected objects across frames.
    """

    def __init__(self, tracker_type, conf_thres=0.5, nms_thres=0.3, conf_decay_rate=0.998):
        """
        Initialize the different attributes required to track objects in pictures.
        :param tracker_type: TrackType. The type of tracker to use. Some are more precise than others, but take more
        CPU/GPU power to run.
        :param conf_thres: Float. The confidence threshold above which an object is considered as detected.
        :param nms_thres: Float. The non-maximum threshold which determines how dissimilar two objects should be to be
        considered as separate.
        :param conf_decay_rate: Float. The rate at which the confidence associated with each object decays. This prevent
        the tracker from drifting too much by virtually making objects disappear and forcing the detector to find the
        object again.
        """

        # Initialize the parent class
        super(ObjectTracker, self).__init__()

        # Tracker, colors, and bonding box management
        self._tracker_type = tracker_type
        self._trackers = {}
        self._colors = {}
        self._bboxes = {}
        self._confidences = {}
        self._next_id = 0

        # Other miscellaneous parameters
        self._conf_decay_rate = conf_decay_rate
        self._conf_thres = conf_thres
        self._nms_thres = nms_thres

        # Initialize a queue in which the next frame to be processed will be put
        self._in_queue = Queue()

        # Initialize a queue in which processed images will be put
        self._out_queue = Queue()

        # Initialize a flag telling the thread when to stop
        self._continue = True

    def run(self):
        while self._continue:
            # Get the next frame from the input queue
            try:
                frame = self._in_queue.get(block=False)

                # Indicate to the input queue that the task has been done
                self._in_queue.task_done()
            except Empty:
                continue

            # Update the bounding boxes of all tracked objects
            dead = self._update(frame)
            # Remove dead objects
            if len(dead) != 0:
                self._remove_trackers(dead)

            # Draw the bounding boxes
            self._draw_bounding_boxes(frame)

            # Make sure the thread was not killed during processing
            if self._continue:
                # Put the processed frame in the output queue
                self._out_queue.put(frame)

    def stop(self):
        """
        Cleanup before destroying the instance.
        :return: None
        """

        # Tell the thread to stop
        self._continue = False

        # Empty the input queue
        print('T: Emptying input queue ...')
        while not self._in_queue.empty():
            self._in_queue.get()
            self._in_queue.task_done()
        # Stop the input queue
        self._in_queue.join()
        print('T: Done.')

        # Empty the output queue
        print('T: Emptying output queue ...')
        while not self._out_queue.empty():
            self._out_queue.get()
            self._out_queue.task_done()
        # Stop the output queue
        self._out_queue.join()
        print('T: Done.')

    def track_objects(self, frame):
        """
        This is a simple wrapper around a Queue.put() method for the input queue of the ObjectTracker.
        It is only here to hide some of the complexities of the implementation.
        The only thing done here is to put the frame given in parameter in the tracker's input queue.
        :param frame: Numpy.ndarray. An array representing the next frame in the video stream.
        :return: None
        """

        # Add the given frame to the input queue to be processed during the next cycle
        self._in_queue.put(frame)

    def get_next_frame(self, block=False, timeout=None):
        """
        Get the next processed frame from the output queue of the tracker.
        :param block: Boolean. If true the call to Queue.get() makes the program pause until a frame
        is available. Otherwise, a frame is returned only if it is present at the right time.
        If no frames are available and block is False, this method raises an Empty exception.
        :param timeout: Float. If not None and block is True, the call to Queue.get() will wait timeout seconds for an
        element to appear in the queue.
        :return: Numpy.ndarray
        """

        # Get the processed frame from the output queue
        frame = self._out_queue.get(block=block)
        # Indicate to the output queue that the task is done
        self._out_queue.task_done()

        # Return the processed frame
        return frame

    def update_trackers(self, bboxes, frame):
        """
        Given the bounding boxes and the frame in parameter update the list of trackers.
        Adding new ones for new objects. No tracker is being removed here this is actually done in the run() method.
        :param bboxes: dict. A dictionary whose keys are the categories of the objects detected, and the values are
        lists of coordinates representing the top-left corner of the bounding box, as well as its size.
        :param frame: Numpy.ndarray. An array corresponding to the frame in which the objects represented by the
        bounding boxes where detected. This is necessary for the trackers to initialize correctly.
        :return: None
        """

        if len(bboxes) != 0:
            # Add previously untracked objects
            for bbox, conf in chain(*bboxes.values()):
                # To check that the object is not already tracked,
                # we compute the IOU. If the iou is over a given
                # threshold, the two boxes are considered to be linked to
                # the same object. This is similar to the NMS algorithm,
                # but without taking the confidences into account.
                for tracked_bbox in self._bboxes.values():
                    # Compute the area of the intersection between the
                    # new object and the tracked object
                    inter_area = max(0, min(bbox[0] + bbox[2],
                                            tracked_bbox[0] + tracked_bbox[2]) - max(bbox[0], tracked_bbox[0])) * \
                                 max(0, min(bbox[1] + bbox[3],
                                            tracked_bbox[1] + tracked_bbox[3]) - max(bbox[1], tracked_bbox[1]))

                    # Compute the area of the new object
                    bbox_area = bbox[2] * bbox[3]
                    # Compute the area of the tracked object
                    tracked_bbox_area = tracked_bbox[2] * tracked_bbox[3]

                    # Finally compute the iou
                    iou = inter_area / (bbox_area + tracked_bbox_area - inter_area)
                    if iou > self._nms_thres:
                        break
                else:
                    # We did not find any similar tracked object,
                    # so this is a new one that should be tracked
                    self._add_trackers(frame, bbox, conf)

    def _draw_bounding_boxes(self, frame):
        # Draw the bounding boxes of all tracked objects
        for obj_id, bbox in self._bboxes.items():
            cv.rectangle(frame, (int(bbox[0]), int(bbox[1])),
                         (int(bbox[0]+bbox[2]), int(bbox[1]+bbox[3])),
                         self._colors[obj_id], thickness=2)

    def _add_trackers(self, frame, bbox, conf):
        # Instantiate and initialize a new tracker for each detected
        # object
        tracker = self._get_tracker()
        # The tuple conversion is required for python < 3.7
        tracker.init(frame, tuple(bbox))

        # Get a unique random color
        color = (randint(0, 255), randint(0, 255), randint(0, 255))
        while color in self._colors.values():
            color = (randint(0, 255), randint(0, 255), randint(0, 255))

        # Store everything related to the object into the
        # corresponding structure
        self._bboxes[self._next_id] = bbox
        self._trackers[self._next_id] = tracker
        self._colors[self._next_id] = color
        self._confidences[self._next_id] = conf

        # Increase the number of objects tracked so far
        self._next_id += 1

    def _remove_trackers(self, obj_ids):
        # Remove everything related to each object in the list
        for obj_id in obj_ids:
            self._trackers.pop(obj_id)
            self._colors.pop(obj_id)
            self._bboxes.pop(obj_id)
            self._confidences.pop(obj_id)

    def _update(self, frame):
        # Declare a list of all the trackers that failed
        dead = []

        # To prevent modifications from happening during processing
        tmp = list(self._trackers.items())

        # Update the bounding boxes of all tracked objects
        for obj_id, tracker in tmp:
            # By default remove any object whose confidence is not above
            # threshold anymore
            if self._confidences[obj_id] < self._conf_thres:
                dead.append(obj_id)
            else:
                # Slowly decay the confidence associated with the object
                self._confidences[obj_id] *= self._conf_decay_rate
                # Update the tracked object's bounding box
                ok, bbox = tracker.update(frame)
                if not ok:
                    # The tracker has failed
                    dead.append(obj_id)
                else:
                    self._bboxes[obj_id] = bbox

        # Return the list of failed trackers
        return dead

    def _get_tracker(self):
        if self._tracker_type == TrackType.MOSSE:
            return cv.legacy.TrackerMOSSE_create()
        if self._tracker_type == TrackType.KCF:
            return cv.TrackerKCF_create()
        if self._tracker_type == TrackType.CSRT:
            return cv.TrackerCSRT_create()

    @property
    def bboxes(self):
        return self._bboxes

    @property
    def confidences(self):
        return self._confidences

    @property
    def colors(self):
        return self._colors

    @property
    def nb_tracked_objects(self):
        return len(self._trackers)
