"""

Behavior classes.

"""

import os
import time
import re
from typing import Dict, List, Optional

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


class MotionProfile:
    __slots__ = [
        "speed",
        "accel",
        "decel",
        "dock_speed",
        "dock_accel",
        "dock_decel",
        "point_turn_speed",
        "point_turn_accel",
        "point_turn_decel",
        "reverse_speed",
    ]

    def __init__(self,
                 speed: float, accel: float, decel: float,
                 dock_speed: float, dock_accel: float, dock_decel: float,
                 point_turn_speed: float, point_turn_accel: float, point_turn_decel: float,
                 reverse_speed: float):

        self.speed = float(speed)
        self.accel = float(accel)
        self.decel = float(decel)
        self.dock_speed = float(dock_speed)
        self.dock_accel = float(dock_accel)
        self.dock_decel = float(dock_decel)
        self.point_turn_speed = float(point_turn_speed)
        self.point_turn_accel = float(point_turn_accel)
        self.point_turn_decel = float(point_turn_decel)
        self.reverse_speed = float(reverse_speed)

    @classmethod
    def from_json(cls, data: Dict):
        return cls(speed=data['speed_mmps'],
                   accel=data['accel_mmps2'],
                   decel=data['decel_mmps2'],
                   dock_speed=data['dockSpeed_mmps'],
                   dock_accel=data['dockAccel_mmps2'],
                   dock_decel=data['dockDecel_mmps2'],
                   point_turn_speed=data['pointTurnSpeed_rad_per_sec'],
                   point_turn_accel=data['pointTurnAccel_rad_per_sec2'],
                   point_turn_decel=data['pointTurnDecel_rad_per_sec2'],
                   reverse_speed=data['reverseSpeed_mmps'])


class SubState:
    __slots__ = [
        "main_turn_chance",
        "body_angle_range_min",
        "body_angle_range_max",
        "relative_body_angle_range_min",
        "relative_body_angle_range_max",
        "head_angle_range_min",
        "head_angle_range_max",
        "head_angle_changes_min",
        "head_angle_changes_max",
        "wait_min",
        "wait_max",
        "wait_anim_trigger",
        "wait_between_changes_min",
        "wait_between_changes_max",
    ]

    def __init__(self,
                 main_turn_chance: Optional[float] = 0.0,
                 body_angle_range_min: Optional[float] = 0.0,
                 body_angle_range_max: Optional[float] = 0.0,
                 relative_body_angle_range_min: Optional[float] = 0.0,
                 relative_body_angle_range_max: Optional[float] = 0.0,
                 head_angle_range_min: Optional[float] = 0.0,
                 head_angle_range_max: Optional[float] = 0.0,
                 head_angle_changes_min: Optional[float] = 0.0,
                 head_angle_changes_max: Optional[float] = 0.0,
                 wait_min: Optional[float] = 0.0,
                 wait_max: Optional[float] = 0.0,
                 wait_anim_trigger: Optional[str] = '',
                 wait_between_changes_min: Optional[float] = 0.0,
                 wait_between_changes_max: Optional[float] = 0.0):
        self.main_turn_chance = float(main_turn_chance) if main_turn_chance is not None else 0.0
        self.body_angle_range_min = float(body_angle_range_min) if body_angle_range_min is not None else 0.0
        self.body_angle_range_max = float(body_angle_range_max) if body_angle_range_max is not None else 0.0
        self.relative_body_angle_range_min = \
            float(relative_body_angle_range_min) if (relative_body_angle_range_min is not None) else 0.0
        self.relative_body_angle_range_max = \
            float(relative_body_angle_range_max) if (relative_body_angle_range_max is not None) else 0.0
        self.head_angle_range_min = float(head_angle_range_min) if head_angle_changes_min is not None else 0.0
        self.head_angle_range_max = float(head_angle_range_max) if head_angle_changes_max is not None else 0.0
        self.wait_min = float(wait_min) if wait_min is not None else 0.0
        self.wait_max = float(wait_max) if wait_max is not None else 0.0
        self.wait_anim_trigger = str(wait_anim_trigger) if wait_anim_trigger is not None else ''
        self.wait_between_changes_min = float(wait_between_changes_min) if wait_between_changes_min is not None else 0.0
        self.wait_between_changes_max = float(wait_between_changes_max) if wait_between_changes_max is not None else 0.0


class BehaviorParameters:
    __slots__ = [
        "should_reset_turn_direction",
        "reset_body_facing_on_start",
        "should_lower_lift",
        "can_carry_cube",
        "distance_from_recent_location",
        "recent_location_max",
        "angle_of_focus",
        "number_of_scans",
        "sequence",
        "motion_profile",
    ]

    def __init__(self,
                 should_reset_turn_direction: bool,
                 reset_body_facing_on_start: bool,
                 should_lower_lift: bool,
                 can_carry_cube: bool,
                 distance_from_recent_location: float,
                 recent_location_max: float,
                 angle_of_focus: float,
                 number_of_scans: int,
                 sequence: List[SubState],
                 motion_profile: Optional[MotionProfile] = None):
        self.should_reset_turn_direction = bool(should_reset_turn_direction)
        self.reset_body_facing_on_start = bool(reset_body_facing_on_start)
        self.should_lower_lift = bool(should_lower_lift)
        self.can_carry_cube = bool(can_carry_cube)
        self.distance_from_recent_location = float(distance_from_recent_location)
        self.recent_location_max = float(recent_location_max)
        self.angle_of_focus = float(angle_of_focus)
        self.number_of_scans = int(number_of_scans)
        self.sequence = sequence
        self.motion_profile = motion_profile

    r = re.compile(r'^s\d_.*')

    @classmethod
    def from_json(cls, data: Dict):
        seq_keys = list(filter(cls.r.match, data.keys()))
        steps = []
        if seq_keys:
            n_steps = int(seq_keys[-1][1]) + 1

            for s in range(n_steps):
                step = SubState(
                    main_turn_chance=data.get('s{}_MainTurnCWChance'.format(s), 0.0),
                    body_angle_range_min=data.get('s{}_BodyAngleRangeMin_deg'.format(s), 0.0),
                    body_angle_range_max=data.get('s{}_BodyAngleRangeMax_deg'.format(s), 0.0),
                    relative_body_angle_range_min=data.get('s{}_BodyAngleRelativeRangeMin_deg'.format(s), 0.0),
                    relative_body_angle_range_max=data.get('s{}_BodyAngleRelativeRangeMax_deg'.format(s), 0.0),
                    head_angle_range_min=data.get('s{}_HeadAngleRangeMin_deg'.format(s), 0.0),
                    head_angle_range_max=data.get('s{}_HeadAngleRangeMax_deg'.format(s), 0.0),
                    head_angle_changes_min=data.get('s{}_HeadAngleChangesMin'.format(s), 0.0),
                    head_angle_changes_max=data.get('s{}_HeadAngleChangesMax'.format(s), 0.0),
                    wait_min=data.get('s{}_WaitMin_sec'.format(s), 0.0),
                    wait_max=data.get('s{}_WaitMax_sec'.format(s), 0.0),
                    wait_anim_trigger=data.get('s{}_WaitAnimTrigger'.format(s), 0.0),
                    wait_between_changes_min=data.get('s{}_WaitBetweenChangesMin_sec'.format(s), 0.0),
                    wait_between_changes_max=data.get('s{}_WaitBetweenChangesMin_sec'.format(s), 0.0))
                steps.append(step)

        mp = MotionProfile.from_json(data['motionProfile']) if 'motionProfile' in data else None

        return cls(should_reset_turn_direction=data.get('behavior_ShouldResetTurnDirection', False),
                   reset_body_facing_on_start=data.get('behavior_ResetBodyFacingOnStart', False),
                   should_lower_lift=data.get('behavior_ShouldLowerLift', False),
                   can_carry_cube=data.get('CanCarryCube', False),
                   distance_from_recent_location=data.get('behavior_DistanceFromRecentLocationMin_mm', 0.0),
                   recent_location_max=data.get('behavior_RecentLocationMax', 0.0),
                   angle_of_focus=data.get('behavior_AngleOfFocus_deg', 0.0),
                   number_of_scans=data.get('behavior_NumberOfScansBeforeStop', 0),
                   motion_profile=mp,
                   sequence=steps)


class Behavior:
    """
    Behavior representation class.

    "requiredUnlockId" is ignored.
    """

    __slots__ = [
        "behavior_class",
        "id",
        "needs_action_id",
        "display_name_key",
        "params",
        "loop_forever",
        "test_gap",
        "runs_per_test",
    ]

    def __init__(self,
                 behavior_class: str,
                 behavior_id: str,
                 needs_action_id: str,
                 display_name_key,
                 params: Optional[BehaviorParameters],
                 loop_forever: Optional[bool] = False,
                 test_gap: Optional[float] = 0.0,
                 runs_per_test: Optional[int] = 1) -> None:
        self.behavior_class = str(behavior_class)
        self.id = str(behavior_id)
        self.needs_action_id = str(needs_action_id)
        self.display_name_key = str(display_name_key)
        self.params = params
        self.loop_forever = bool(loop_forever)
        self.test_gap = float(test_gap) if test_gap is not None else 0.0
        self.runs_per_test = int(runs_per_test) if runs_per_test is not None else 1

    @classmethod
    def from_json(cls, data: Dict):
        return cls(behavior_class=data['behaviorClass'],
                   behavior_id=data['behaviorID'],
                   needs_action_id=data.get('needsActionID', ''),
                   display_name_key=data.get('displayNameKey', ''),
                   params=BehaviorParameters.from_json(data.get('params')) if 'params' in data else None,
                   loop_forever=data.get('loopForever', False),
                   test_gap=data.get('gapBetweenTests_s', 0.0),
                   runs_per_test=data.get('nRunsPerTest', 1))


def load_behaviors(resource_dir: str) -> Dict[str, Behavior]:

    start_time = time.time()

    behavior_files = get_json_files(resource_dir,
                                    [os.path.join('cozmo_resources', 'config', 'engine',
                                                  'behaviorSystem', 'behaviors')])
    behaviors = {}

    for filename in behavior_files:
        json_data = load_json_file(filename)
        behaviors[json_data['behaviorID']] = Behavior.from_json(json_data)

    logger.debug("Loaded {} behaviors in {:.02f} s.".format(len(behaviors), time.time() - start_time))

    return behaviors


def load_reaction_trigger_behavior_map(resource_dir: str) -> Dict[str, ReactionTrigger]:

    start_time = time.time()

    reaction_trigger_behavior_map = {}
    filename = os.path.join(resource_dir, 'cozmo_resources', 'config',
                            'engine', 'behaviorSystem', 'reactionTrigger_behavior_map.json')

    json_data = load_json_file(filename)
    for trigger in json_data['reactionTriggerBehaviorMap']:
        reaction_trigger_behavior_map[trigger['reactionTrigger']] = ReactionTrigger.from_json(trigger)

    logger.debug("Loaded {} entry reaction trigger behavior map in {:.02f} s.".format(
        len(reaction_trigger_behavior_map), time.time() - start_time))

    return reaction_trigger_behavior_map
