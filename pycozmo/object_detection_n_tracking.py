#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import path
from pycozmo.object_tracker import ObjectTracker
from pycozmo.object_detector import ObjectDetector


# TODO: Replace this monstrosity with util.get_cozmo_asset_dir()
#       or util.get_cozmo_dir(), depending on where the weights
#       and such configuration should live.
BASE_DIR = path.abspath(path.dirname(__file__))


class ObjectDetectionNTracking(object):
    """
    A simple class that uses both an ObjectDetector to detect objects in a frame and multiple ObjectTrackers to track
    detected objects across frames.
    """

    def __init__(self, tracker_type, skip_frames, obj_cats, conf_thres=0.5, nms_thres=0.3,
                 conf_decay_rate=0.998, img_w=704, img_h=704,
                 classes_name_file=path.join(BASE_DIR, 'trackerCfg', 'openimages.names'),
                 model_conf_file=path.join(BASE_DIR, 'trackerCfg', 'yolo.cfg'),
                 model_weight_file=path.join(BASE_DIR, 'trackerCfg', 'yolo.weights')):
        """
        Initialize the different attributes required to detect and track objects in pictures.
        :param tracker_type: TrackType. The type of tracker to use. Some are more precise than others, but take more
        CPU/GPU power to run.
        :param skip_frames: Int. The number of frames to skip in-between two detection event. Since running YoloV4 might
        take quite a lot of GPU power it can be interesting for low-spec computers to only run the detection algorithm
        every so often.
        :param obj_cats: List. A list of categories of objects to detect and track in every picture.
        :param conf_thres: Float. The confidence threshold above which an object is considered as detected.
        :param nms_thres: Float. The non-maximum threshold which determines how dissimilar two objects should be to be
        considered as separate.
        :param conf_decay_rate: Float. The rate at which the confidence associated with each object decays. This prevent
        the tracker from drifting too much by virtually making objects disappear and forcing the detector to find the
        object again.
        :param img_w: Int. The width of the frame passed to the detector network. This size should be a multiple of 32.
        :param img_h: Int. The height of the frame passed to the detector network. This size should be a multiple of 32.
        :param classes_name_file: String. The relative path to the text file containing the name of the categories of
        object to be detected.
        :param model_conf_file: String. The relative path to the file containing the configuration of the YoloV4 network
        to be used as the object detector.
        :param model_weight_file: String. The relative path to the file containing the pre-trained weights for the
        detector network.
        """

        # Initialize the parent class
        super(ObjectDetectionNTracking, self).__init__()

        # How many frames to skip between detection
        assert skip_frames > 0, "The number of frames skipped between " \
                                "detection event should be greater than or " \
                                "equal to 1."
        self._skip_frames = skip_frames
        self._frame_cpt = 0

        # Get an object tracker
        self._tracker = ObjectTracker(tracker_type, conf_thres, nms_thres, conf_decay_rate)

        # Get an object detector
        self._detector = ObjectDetector(obj_cats, conf_thres, nms_thres, img_w, img_h, classes_name_file,
                                        model_conf_file, model_weight_file)

        # Add the tracker's update_trakers() function as a listener to the detector
        self._detector.add_listener(self._tracker.update_trackers)

        # Start both the tracker and detector
        self._tracker.start()
        self._detector.start()

    def process_frame(self, frame):
        """
        Capture next frame from video device and hand it to both the ObjectTracker, and ObjectDetector
        (when appropriate).
        :param frame: numpy.ndarray. An array representing the frame to be processed by both the detector and tracker.
        :return: None
        """

        # Pass the new frame to the tracker
        self._tracker.track_objects(frame)

        # On the very first frame, or if no object is currently tracked,
        # or on the nth frame
        # /!\ Never reinitialize the number of skipped frames
        if self._frame_cpt == 0 or self._tracker.nb_tracked_objects == 0 or \
                self._frame_cpt % self._skip_frames == 0:
            # Pass the new frame to the detector
            self._detector.detect_objects(frame)

        # Increase the number of frames processed
        self._frame_cpt += 1

    def get_next_frame(self, block=False, timeout=None):
        """
        Get the next processed from from the ObjectTracker directly.
        This method is not really required and adds layers to an already high cake,
        but it hides away the 'complexities' of the implementation.
        :param block: Boolean. If true the call to Queue.get() makes the program pause until a frame
        is available. Otherwise, a frame is returned only if it is present at the right time.
        If no frames are available and block is False, this method raises an Empty exception.
        :param timeout: Float. If not None and block is True, the call to Queue.get() will wait timeout seconds for an
        element to appear in the queue.
        :return: None
        """
        # Return next processed frame from the tracker
        return self._tracker.get_next_frame(block=block, timeout=timeout)

    def stop(self):
        """
        Cleanup before destroying the instance.
        :return: None
        """

        # Ask the tracker to stop
        self._tracker.stop()
        self._tracker.join()

        # Ask the detector to stop
        self._detector.stop()
        self._detector.join()
