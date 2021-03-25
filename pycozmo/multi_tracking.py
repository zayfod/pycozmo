#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import uname
from random import randint
from enum import IntEnum
from itertools import chain
import numpy as np
import cv2 as cv


class ObjCat(IntEnum):
    HAND = 0
    HEAD = 1


class TrackType(IntEnum):
    CSRT = 0
    KCF = 1
    MOSSE = 2


class MultiTracker:
    """
    A personal implementation of a multi-object tracker for the OpenCV library.
    """

    def __init__(self, tracker_type: TrackType, skip_frames,
                 obj_cats, conf_thres=0.5, nms_thres=0.3, conf_decay_rate=0.998,
                 img_w=704,
                 img_h=704, classes_name_file='openimages.names',
                 model_conf_file='yolo.cfg', model_weight_file='yolo.weights'):

        # How many frames to skip between detection
        assert skip_frames > 0, "The number of frames skipped between " \
                                "detection event should be greater than or " \
                                "equal to 1."
        self._skip_frames = skip_frames
        self._frame_cpt = 0
        # Tracker, colors, and bonding box management
        self._tracker_type = tracker_type
        self._trackers = {}
        self._colors = {}
        self._bboxes = {}
        self._confidences = {}
        self._next_id = 0

        # Classes and categories management
        self._tracked_cats = obj_cats
        self._avail_classes = []
        with open(classes_name_file, 'rt') as f:
            self._avail_classes = f.read().rstrip('\n').split('\n')

        # Yolo parameters
        self._conf_thres = conf_thres
        self._nms_thres = nms_thres
        self._img_size = (img_w, img_h)

        # Other miscellaneous parameters
        self._conf_decay_rate = conf_decay_rate

        # Instantiate a yolo-based object detection network
        self._dnn = cv.dnn.readNetFromDarknet(model_conf_file,
                                              model_weight_file)
        self._dnn.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
        self._dnn.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)
        # Get the name of the output layers
        self._out_layers_name = [self._dnn.getLayerNames()[i[0] - 1] for i in
                                 self._dnn.getUnconnectedOutLayers()]

    def step(self, frame):
        # Update the bounding boxes of all tracked objects
        dead = self._update(frame)
        # Remove dead objects
        if len(dead) != 0:
            self._untrack_objects(dead)

        # On the very first frame, or if no object is currently tracked,
        # or on the nth frame
        # /!\ Never reinitialize the number of skipped frames
        if self._frame_cpt == 0 or len(self._trackers) == 0 or self._frame_cpt % self._skip_frames == 0:
            # Detect objects and extract corresponding bboxes
            outs = self._detect(frame)
            frame_h, frame_w = frame.shape[0:2]
            bboxes = self._extract_bboxes(outs, frame_w, frame_h)

            # Rather than stop if the detector has not found anything,
            # we simply continue with what we have
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
                        inter_area = max(0, min(bbox[0] + bbox[2], tracked_bbox[0]+tracked_bbox[2]) - max(bbox[0], tracked_bbox[0])) * \
                                     max(0, min(bbox[1]+bbox[3], tracked_bbox[1]+tracked_bbox[3]) - max(bbox[1], tracked_bbox[1]))

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
                        self._track_object(frame, bbox, conf)

        # Increase the number of frames processed
        self._frame_cpt += 1

    def draw_bounding_boxes(self, frame):
        # Draw the bounding boxes of all tracked objects
        for obj_id, bbox in self._bboxes.items():
            cv.rectangle(frame, (int(bbox[0]), int(bbox[1])),
                         (int(bbox[0]+bbox[2]), int(bbox[1]+bbox[3])),
                         self._colors[obj_id], thickness=2)

    def _track_object(self, frame, bbox, conf):
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

    def _untrack_objects(self, obj_ids):
        # Remove everything related to each object in the list
        for obj_id in obj_ids:
            self._trackers.pop(obj_id)
            self._colors.pop(obj_id)
            self._bboxes.pop(obj_id)
            self._confidences.pop(obj_id)

    def _update(self, frame):
        # Declare a list of all the trackers that failed
        dead = []

        # Update the bounding boxes of all tracked objects
        for obj_id, tracker in self._trackers.items():
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

    @property
    def bboxes(self):
        return self._bboxes

    @property
    def confidences(self):
        return self._confidences

    @property
    def colors(self):
        return self._colors


if __name__ == "__main__":
    machine = uname().machine
    # Initialize the video capturing device and the multi-tracker based on
    # the processor type
    if machine == 'aarch64' or machine.startswith('arm'):
        video = cv.VideoCapture('nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3264, height=2464, format=(string)NV12, framerate=21/1 ! nvvidconv flip-method=2 ! video/x-raw, width=960, height=616, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink', cv.CAP_GSTREAMER)

        multi_tracker = MultiTracker(TrackType.MOSSE, skip_frames=5,
                                     obj_cats=[ObjCat.HAND, ObjCat.HEAD])
    else:
        video = cv.VideoCapture(0)
        multi_tracker = MultiTracker(TrackType.KCF, skip_frames=5,
                                     obj_cats=[ObjCat.HAND, ObjCat.HEAD])

    # Make sure we have access to the video capturing device
    if not video.isOpened():
        print('Could not open the video capturing device.')
        exit(-1)

    # Start processing frames
    try:
        while True:
            # Read the next frame
            ok, frame = video.read()
            if not ok:
                print('No more frames to process. End of the stream?')
                break

            # Step though the tracking sequence
            multi_tracker.step(frame)

            # Draw the bounding boxes
            multi_tracker.draw_bounding_boxes(frame)

            # Display the resulting frame
            cv.imshow('Multi-Tracker', frame)

            # Check if the use wants to quit
            if cv.waitKey(1) == ord('q'):
                break
    finally:
        video.release()
        cv.destroyAllWindows()
