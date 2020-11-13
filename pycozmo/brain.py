"""

Brain class - high level behavior and emotion engine.

"""

from typing import Optional
from threading import Thread
from queue import Queue, Empty
import time

from . import logger, logger_reaction, logger_behavior
from . import client
from . import event
from . import emotions
from . import behavior
from . import activity
from . import util
from . import robot


__all__ = [
    "Brain"
]


class Brain:
    """ Cozmo robot brain class. """

    def __init__(self, cli: client.Client):
        super().__init__()

        self.cli = cli

        # TODO: Load configuration. See cozmo_resources/config/features.json

        util.check_assets()

        start_time = time.perf_counter()
        resource_dir = str(util.get_cozmo_asset_dir())
        self.activities = activity.load_activities(resource_dir)
        self.behaviors = behavior.load_behaviors(resource_dir, self.cli)
        self.reaction_trigger_beahvior_map = behavior.load_reaction_trigger_behavior_map(resource_dir)
        self.emotion_types = emotions.load_emotion_types(resource_dir)
        self.emotion_events = emotions.load_emotion_events(resource_dir)
        self.cli.load_anims()
        logger.info("Loaded resources in {:.02f} s.".format(time.perf_counter() - start_time))

        self.cli.add_handler(event.EvtBehaviorDone, self.on_behavior_done)
        self.cli.add_handler(event.EvtCliffDetectedChange, self.on_cliff_detected)
        self.cli.add_handler(event.EvtRobotOrientationChange, self.on_robot_orientation_change)
        self.cli.add_handler(event.EvtRobotPickedUpChange, self.on_robot_picked_up_change)
        self.cli.add_handler(event.EvtRobotFallingChange, self.on_robot_falling_change)
        self.cli.add_handler(event.EvtRobotOnChargerChange, self.on_robot_on_charger_change)
        # TODO: ...

        # Reaction trigger queue
        self.reaction_queue = Queue()

        self.stop_flag = False
        self.reaction_thread = Thread(daemon=True, name="ReactionThread", target=self.reaction_thread_run)
        self.heartbeat_thread = Thread(daemon=True, name="HeartbeatThread", target=self.heartbeat_thread_run)

        # Current activity
        self.activity = self.activities["Freeplay"]
        # Current behavior
        self.behavior = None    # type: Optional[behavior.Behavior]

    def start(self):
        # Connect to robot
        self.reaction_thread.start()
        self.heartbeat_thread.start()

        # TODO: Enable stop on cliff.
        # TODO: Enable camera.
        # TODO: Drive off if on charger.

    def stop(self):
        # Disconnect from robot
        self.stop_flag = True
        if self.heartbeat_thread:
            self.heartbeat_thread.join()
            self.heartbeat_thread = None
        if self.reaction_thread:
            self.reaction_thread.join()
            self.reaction_thread = None

    def on_behavior_done(self, cli: client.Client) -> None:
        if self.behavior:
            logger_reaction.info("Done.")
            self.deactivate_behavior()

    def on_cliff_detected(self, cli: client.Client, state: bool) -> None:
        if state and not cli.robot_picked_up and cli.robot_moving:
            self.post_reaction("CliffDetected")

    def on_robot_orientation_change(self, cli: client.Client, orientation: robot.RobotOrientation) -> None:
        # FIXME: These are not working well at present.
        # if orientation == robot.RobotOrientation.ON_THREADS:
        #     self.post_reaction("ReturnedToTreads")
        # elif orientation == robot.RobotOrientation.ON_BACK:
        #     self.post_reaction("RobotOnBack")
        # elif orientation == robot.RobotOrientation.ON_FACE:
        #     self.post_reaction("RobotOnFace")
        # elif orientation == robot.RobotOrientation.ON_LEFT_SIDE or \
        #         orientation == robot.RobotOrientation.ON_RIGHT_SIDE:
        #     self.post_reaction("RobotOnSide")
        pass

    def on_robot_picked_up_change(self, cli: client.Client, state: bool) -> None:
        if state:
            self.post_reaction("RobotPickedUp")

    def on_robot_falling_change(self, cli: client.Client, state: bool):
        if state:
            self.post_reaction("RobotFalling")

    def on_robot_on_charger_change(self, cli: client.Client, state: bool) -> None:
        if state:
            self.post_reaction("PlacedOnCharger")

    def on_camera_image(self, cli: client.Client, new_im) -> None:
        """ Process images, coming from the robot camera. """
        # TODO: See cozmo_resources/config/engine/vision_config.json
        # TODO: motion detection
        # self.process_reaction_trigger("UnexpectedMovement")
        # TODO: face detection
        # self.process_reaction_trigger("FacePositionUpdate")?
        # TODO: pet detection
        # self.process_reaction_trigger("PetInitialDetection")
        # TODO: laser detection
        # TODO: cube marker detection
        # TODO: facial expression estimation
        # TODO: smile amount detection
        # TODO: blink amount detection
        # TODO: gaze detection?
        # TODO: image quality check
        pass

    def post_reaction(self, reaction_trigger: str) -> None:
        """ Post a reaction trigger to the reaction trigger queue. """
        logger_reaction.debug("Posting {}".format(reaction_trigger))
        self.reaction_queue.put(reaction_trigger)

    def reaction_thread_run(self) -> None:
        """ Reaction thread loop. Reaction trigger queue processing. """
        while not self.stop_flag:
            try:
                reaction_trigger = self.reaction_queue.get(timeout=0.05)
            except Empty:
                continue
            except Exception as e:
                logger.error("Failed to get from reaction trigger queue. {}".format(e))
                continue

            try:
                logger_reaction.info("Processing {}".format(reaction_trigger))
                self.process_emotion_event(reaction_trigger)
                self.process_reaction(reaction_trigger)
            except Exception as e:
                logger.error("Failed to dispatch reaction trigger '{}'. {}".format(reaction_trigger, e))
                continue

    def process_emotion_event(self, reaction_trigger: str) -> None:
        """ Process emotion events by applying affectors to emotion types. """
        emotion_event = self.emotion_events.get(reaction_trigger)
        if emotion_event:
            for affector, delta in emotion_event.affectors.items():
                self.emotion_types[affector].add(delta)
        else:
            logger_reaction.warning("Failed to find emotion event for {}.".format(reaction_trigger))

    def process_reaction(self, reaction_trigger: str) -> None:
        reaction = self.reaction_trigger_beahvior_map.get(reaction_trigger)
        if reaction:
            # TODO: Handle should_resume_last.
            self.activate_behavior(reaction.behavior_id)
        else:
            logger_reaction.error("Failed to find reaction for {}.".format(reaction_trigger))

    def activate_behavior(self, behavior_id: str) -> None:
        behavior = self.behaviors.get(behavior_id)
        if behavior:
            self.deactivate_behavior()
            logger_behavior.info("Activating {}".format(behavior_id))
            self.behavior = behavior
            self.cli.activate_behavior(self.behavior)
        else:
            logger_reaction.error("Failed to find behavior {}.".format(behavior_id))

    def deactivate_behavior(self) -> None:
        if self.behavior:
            logger_behavior.info("Deactivating {}".format(self.behavior.get_id()))
            self.cli.deactivate_behavior(self.behavior)
            self.behavior = None
            # TODO: Choose behavior from activity?

    def heartbeat_thread_run(self) -> None:
        """ Heartbeat thread loop. """

        # Raise head.
        angle = (robot.MAX_HEAD_ANGLE.radians - robot.MIN_HEAD_ANGLE.radians) / 2.0
        self.cli.set_head_angle(angle)

        cnt = 1
        timer = util.FPSTimer(robot.FRAME_RATE)
        while not self.stop_flag:

            self.update_emotion_types()
            # TODO: Timers

            if cnt % (30 * 60) == 0:
                self.post_reaction("Hiccup")

            cnt += 1
            timer.sleep()

    def update_emotion_types(self) -> None:
        """ Update emotion types from their decay functions. """
        for emotion_type in self.emotion_types.values():
            emotion_type.update()
