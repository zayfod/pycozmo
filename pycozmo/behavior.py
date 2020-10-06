"""

Behavior classes.

"""
import re
from typing import Dict, List, Optional

from .json_loader import get_json_files, load_json_file


__all__ = [
    "ReactionTrigger",
    "Behavior",

    "load_behaviors",
    "load_reaction_trigger_behavior_map",
]


class ReactionTrigger:
    """ Reaction trigger representation class. """
    def __init__(self, name: str, behavior_id: str, should_resume_last: Optional[bool] = False):
        self.name = str(name)
        self.behavior_id = behavior_id
        self.should_resume_last = should_resume_last

    @classmethod
    def from_json(cls, data: Dict):
        return cls(name=data['reactionTrigger'],
                   behavior_id=data['behaviorID'],
                   should_resume_last=data.get('genericStrategyParams').get('shouldResumeLast'))


class MotionProfile:
    def __init__(self,
                 speed: float, accel: float, decel: float,
                 dock_speed: float, dock_accel: float, dock_decel: float,
                 point_turn_speed: float, point_turn_accel: float, point_turn_decel: float,
                 reverse_speed: float):

        self.speed = speed
        self.accel = accel
        self.decel = decel
        self.dock_speed = dock_speed
        self.dock_accel = dock_accel
        self.dock_decel = dock_decel
        self.point_turn_speed = point_turn_speed
        self.point_turn_accel = point_turn_accel
        self.point_turn_decel = point_turn_decel
        self.reverse_speed = reverse_speed

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
        self.main_turn_chance = main_turn_chance
        self.body_angle_range_min = body_angle_range_min
        self.body_angle_range_max = body_angle_range_max
        self.relative_body_angle_range_min = relative_body_angle_range_min
        self.relative_body_angle_range_max = relative_body_angle_range_max
        self.head_angle_range_min = head_angle_range_min
        self.head_angle_range_max = head_angle_range_max
        self.wait_min = wait_min
        self.wait_max = wait_max
        self.wait_anim_trigger = wait_anim_trigger
        self.wait_between_changes_min = wait_between_changes_min
        self.wait_between_changes_max = wait_between_changes_max


class BehaviorParameters:
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
        self.should_reset_turn_direction = should_reset_turn_direction
        self.reset_body_facing_on_start = reset_body_facing_on_start
        self.should_lower_lift = should_lower_lift
        self.can_carry_cube = can_carry_cube
        self.distance_from_recent_location = distance_from_recent_location
        self.recent_location_max = recent_location_max
        self.angle_of_focus = angle_of_focus
        self.number_of_scans = number_of_scans
        self.motion_profile = motion_profile
        self.sequence = sequence

    @classmethod
    def from_json(cls, data: Dict):
        r = re.compile('^s\d_.*')
        seq_keys = list(filter(r.match, data.keys()))
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
    ]

    def __init__(self,
                 behavior_class: str,
                 behavior_id: str,
                 needs_action_id: str,
                 display_name_key,
                 params: BehaviorParameters) -> None:
        self.behavior_class = str(behavior_class)
        self.id = str(behavior_id)
        self.needs_action_id = str(needs_action_id)
        self.display_name_key = str(display_name_key)
        self.params = params

    @classmethod
    def from_json(cls, data: Dict):
        return cls(behavior_class=data['behaviorClass'],
                   behavior_id=data['behaviorID'],
                   needs_action_id=data.get('needsActionID', ''),
                   display_name_key=data.get('displayNameKey', ''),
                   params=BehaviorParameters.from_json(data.get('params')) if 'params' in data else None)


class TestBehavior:
    def __init__(self,
                 behavior_class: str,
                 behavior_id: str,
                 loop_forever: Optional[bool] = False,
                 test_gap: Optional[float] = 0.0,
                 runs_per_test: Optional[int] = 1) -> None:
        self.behavior_class = str(behavior_class)
        self.id = str(behavior_id)
        self.loop_forever = loop_forever
        self.test_gap = test_gap
        self.runs_per_test = runs_per_test

    @classmethod
    def from_json(cls, data: Dict):
        return cls(behavior_class=data['behaviorClass'],
                   behavior_id=data['behaviorID'],
                   loop_forever=data.get('loopForever', False),
                   test_gap=data.get('gapBetweenTests_s', 0.0),
                   runs_per_test=data.get('nRunsPerTest', 1))


def load_behaviors(resource_dir: str) -> Dict[str, Behavior]:
    behavior_files = get_json_files(resource_dir,
                                    ['/cozmo_resources/config/engine/behaviorSystem/behaviors/'])
    behaviors = {}

    for filename in behavior_files:
        json_data = load_json_file(filename)
        if 'Test' not in json_data['behaviorID']:
            behaviors[json_data['behaviorID']] = Behavior.from_json(json_data)
    return behaviors


def load_test_behaviors(resource_dir: str) -> Dict[str, Behavior]:
    behavior_files = get_json_files(resource_dir,
                                    ['/cozmo_resources/config/engine/behaviorSystem/behaviors/'])
    behaviors = {}

    for filename in behavior_files:
        json_data = load_json_file(filename)
        if 'Test' in json_data['behaviorID']:
            behaviors[json_data['behaviorID']] = TestBehavior.from_json(json_data)
    return behaviors


def load_reaction_trigger_behavior_map(resource_dir: str) -> Dict[str, ReactionTrigger]:
    reaction_trigger_behavior_map = {}
    filename = resource_dir + \
        '/cozmo_resources/config/engine/behaviorSystem/reactionTrigger_behavior_map.json'

    json_data = load_json_file(filename)
    for trigger in json_data['reactionTriggerBehaviorMap']:
        reaction_trigger_behavior_map[trigger['reactionTrigger']] = ReactionTrigger.from_json(trigger)

    return reaction_trigger_behavior_map
