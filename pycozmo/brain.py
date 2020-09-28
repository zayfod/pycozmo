"""

Brain class.

"""

from threading import Thread
from queue import Queue, Empty
import time

from . import logger
from . import event
from . import emotions
from . import behavior
from . import activity
from . import anim
from . import util


__all__ = [
    "Brain"
]


class Brain:
    """ Cozmo robot brain class. """

    def __init__(self, cli):
        super().__init__()

        self.activities = activity.load_activities()
        self.behaviors = behavior.load_behaviors()
        self.reaction_trigger_beahvior_map = behavior.load_reaction_trigger_behavior_map()
        self.animation_groups = anim.load_animation_groups()    # TODO: Move to Client?
        self.emotion_types = emotions.load_emotion_types()
        self.emotion_events = emotions.load_emotion_events()

        self.cli = cli
        self.cli.load_anims(str(util.get_cozmo_anim_dir()))
        self.cli.add_handler(event.EvtCliffDetectedChange, self.on_cliff_detected)
        # TODO: ...

        # Reaction trigger queue
        self.reaction_queue = Queue()

        self.stop_flag = False
        self.reaction_thread = Thread(daemon=True, name="ReactionThread", target=self.reaction_thread_run)
        self.heartbeat_thread = Thread(daemon=True, name="HeartbeatThread", target=self.heartbeat_thread_run)

    def start(self):
        # Connect to robot
        self.reaction_thread.start()
        self.heartbeat_thread.start()

        # TODO: Enable camera

    def stop(self):
        # Disconnect from robot
        self.stop_flag = True
        self.heartbeat_thread.join()
        self.reaction_thread.join()

    def on_cliff_detected(self, cli, state: bool) -> None:
        if state:
            self.post_reaction("CliffDetected")

    def on_camera_image(self, cli, new_im) -> None:
        """ Process images, coming from the robot camera. """
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
        self.reaction_queue.put(reaction_trigger)

    def reaction_thread_run(self) -> None:
        """ Reaction thread loop. Reaction trigger queue processing. """
        while not self.stop_flag:
            try:
                reaction_trigger = self.reaction_queue.get(timeout=0.05)
                self.reaction_queue.task_done()
            except Empty:
                continue
            except Exception as e:
                logger.error("Failed to get from reaction trigger queue. {}".format(e))
                continue

            try:
                self.process_reaction(reaction_trigger)
            except Exception as e:
                logger.error("Failed to dispatch reaction trigger '{}'. {}".format(reaction_trigger, e))
                continue

    def process_reaction(self, reaction_trigger: str) -> None:
        # TODO: Look up in reaction trigger behavior map and call activate_behavior()
        pass

    def activate_behavior(self, behavior_id: str) -> None:
        # TODO: Look up in behavior map and call play_anim_group
        pass

    def play_anim_group(self, anim_group_name: str) -> None:
        # TODO: Look up in animation groups and choose animation.
        anim_name = "test"
        self.cli.play_anim(anim_name)

    def heartbeat_thread_run(self) -> None:
        """ Heartbeat thread loop. """

        cnt = 1
        while not self.stop_flag:

            self.update_emotion_types()
            self.update_face()
            # TODO: hiccups
            if cnt % (30 * 60) == 0:
                self.post_reaction("Hiccup")

            cnt += 1
            time.sleep(1/30)

    def update_emotion_types(self) -> None:
        """ Update emotion types from their decay functions. """
        for emotion_type in self.emotion_types.values():
            emotion_type.update()

    def update_face(self) -> None:
        """ Procedural face update when an animation is not running. """
        pass
