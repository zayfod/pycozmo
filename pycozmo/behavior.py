"""

Behavior representation and reading.

"""

import os
import time
from typing import Dict, Optional, Any

from . import event
from . import client
from . import logger
from .json_loader import get_json_files, load_json_file


__all__ = [
    "ReactionTrigger",
    "Behavior",

    "load_behaviors",
    "load_reaction_trigger_behavior_map",
]


class ReactionTrigger:
    """ Reaction trigger representation class. """
    __slots__ = [
        "name",
        "behavior_id",
        "should_resume_last",
    ]

    def __init__(self, name: str, behavior_id: str, should_resume_last: Optional[bool] = False):
        self.name = str(name)
        self.behavior_id = str(behavior_id)
        self.should_resume_last = bool(should_resume_last)

    @classmethod
    def from_json(cls, data: Dict):
        return cls(name=data['reactionTrigger'],
                   behavior_id=data['behaviorID'],
                   should_resume_last=data.get('genericStrategyParams', {}).get('shouldResumeLast'))


class Behavior(event.Dispatcher):
    """ Behavior representation class. """

    def __init__(self, cli: client.Client, conf: Any) -> None:
        super().__init__()
        self.cli = cli
        self.conf = conf

    def get_id(self) -> str:
        return self.conf["behaviorID"]

    def activate(self) -> None:
        logger.warning("Behavior '{}' not implemented.".format(self.get_id()))
        self.cli.conn.post_event(event.EvtBehaviorDone, self.cli)

    def deactivate(self) -> None:
        pass


class BehaviorPlayAnim(Behavior):
    """ Play a sequence of animation triggers. """

    def __init__(self, cli: client.Client, conf: Any):
        super().__init__(cli, conf)
        self.anim_triggers = conf.get("animTriggers", [])
        self.current_trigger = 0
        self.add_handler(event.EvtAnimationCompleted, self._on_animation_completed)

    def activate(self) -> None:
        self.current_trigger = 0
        if self.anim_triggers:
            anim_trigger = self.anim_triggers[self.current_trigger]
            self.current_trigger += 1
            self.cli.play_anim_group(anim_trigger)

    def _on_animation_completed(self, cli):
        # TODO: Support additional animation triggers.
        self.cli.conn.post_event(event.EvtBehaviorDone, self.cli)

    def deactivate(self) -> None:
        self.cli.cancel_anim()


class BehaviorPlayArbitraryAnim(BehaviorPlayAnim):
    """ Play a random animation trigger. """

    def activate(self) -> None:
        # TODO: Pick random animation trigger and put it in sequence
        super().activate()


class BehaviorReactToCliff(BehaviorPlayAnim):
    """ ReactToCliff behavior - currently, just plays animation. """

    def activate(self) -> None:
        self.anim_triggers = ("ReactToCliff", )
        super().activate()


class BehaviorDriveOffCharger(Behavior):

    def activate(self) -> None:
        # extraDistanceToDrive_mm = float(self.conf["extraDistanceToDrive_mm"])
        # TODO: Play wake up animation?
        # TODO: Drive and wait for completion.
        self.cli.conn.post_event(event.EvtBehaviorDone, self.cli)

    def deactivate(self) -> None:
        # TODO: Cancel
        pass


def get_behavior_class_from_dict(data):
    """ Choose a behavior class, based on the behaviorClass JSON attribute. """
    # TODO: Replace with a behavior package.
    class_map = {
        "PlayAnim": BehaviorPlayAnim,
        "PlayArbitraryAnim": BehaviorPlayArbitraryAnim,
        "ReactToCliff": BehaviorReactToCliff,
        "DriveOffCharger": BehaviorDriveOffCharger,
    }
    cls = class_map.get(data["behaviorClass"], Behavior)
    return cls


def load_behaviors(resource_dir: str, cli: client.Client) -> Dict[str, Behavior]:

    start_time = time.perf_counter()

    behavior_files = get_json_files(
        resource_dir, [os.path.join('cozmo_resources', 'config', 'engine', 'behaviorSystem', 'behaviors')])
    behaviors = {}
    for filename in behavior_files:
        data = load_json_file(filename)
        cls = get_behavior_class_from_dict(data)
        behaviors[data['behaviorID']] = cls(cli, data)

    logger.debug("Loaded {} behaviors in {:.02f} s.".format(len(behaviors), time.perf_counter() - start_time))

    return behaviors


def load_reaction_trigger_behavior_map(resource_dir: str) -> Dict[str, ReactionTrigger]:

    start_time = time.perf_counter()

    reaction_trigger_behavior_map = {}
    filename = os.path.join(resource_dir, 'cozmo_resources', 'config',
                            'engine', 'behaviorSystem', 'reactionTrigger_behavior_map.json')

    json_data = load_json_file(filename)
    for trigger in json_data['reactionTriggerBehaviorMap']:
        reaction_trigger_behavior_map[trigger['reactionTrigger']] = ReactionTrigger.from_json(trigger)

    logger.debug("Loaded {} entry reaction trigger behavior map in {:.02f} s.".format(
        len(reaction_trigger_behavior_map), time.perf_counter() - start_time))

    return reaction_trigger_behavior_map
