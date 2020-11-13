"""

Activity representation and reading.

"""

import os
import time
from typing import Dict, List, Optional

import numpy as np

from . import logger
from .emotions import DecayGraph, Node
from .json_loader import get_json_files, load_json_file


__all__ = [
    "Activity",

    "load_activities",
]


class BehaviorChooser:
    __slots__ = [
        "choice_type",
        "behaviors",
        "iteration",
        "__dict__",
    ]

    def __init__(self,
                 choice_type: str,
                 behaviors: List) -> None:

        self.choice_type = str(choice_type)
        self.behaviors = behaviors

        if self.choice_type == 'Scoring':
            self.init_scores()
            self.init_repetition_penalty()

    @classmethod
    def from_json(cls, data: Dict):
        return cls(
            choice_type=data['type'],
            behaviors=data.get('behaviors', [])
        )

    def reset(self):
        self.iteration = 0
        self.init_scores()

    def init_scores(self) -> None:
        self.behavior_scores = []
        self.behavior_names = []
        self.behavior_repetitions = []
        for b in self.behaviors:
            self.behavior_scores.append(b['scoring']['flatScore'])
            self.behavior_names.append(b['behaviorID'])
            self.behavior_repetitions.append(0)
        self.total_score = sum(self.behavior_scores)

    def init_repetition_penalty(self) -> None:
        self.repetition_penalties = []
        for b in self.behaviors:
            if 'repetitionPenalty' in b['scoring']:
                self.repetition_penalties.append(
                    DecayGraph([Node(x=n['x'], y=n['y']) for n in b['scoring']['repetitionPenalty']['nodes']]))
            else:
                self.repetition_penalties.append(DecayGraph([Node(x=1, y=0)]))

    def apply_repetition_penalty(self, ref) -> None:
        if self.choice_type == 'Scoring':
            if isinstance(ref, str):
                idx = self.behavior_names.index(ref)
            elif isinstance(ref, int):
                idx = ref
            else:
                raise TypeError('Invalid behavior index: {}'.format(ref))
            self.behavior_repetitions[idx] += 1
            self.behavior_scores[idx] -= self.repetition_penalties[idx].evaluate(self.behavior_repetitions[idx])
            self.behavior_scores[idx] = max(0, self.behavior_scores[idx])
            self.total_score = sum(self.behavior_scores)

    def get_sorted_choices(self) -> List[str]:
        if self.choice_type == 'Selection':
            return None
        if self.choice_type == 'StrictPriority':
            if self.iteration <= len(self.behaviors):
                return self.behaviors
            else:
                return None
        elif self.choice_type == 'Scoring':
            if self.behavior_names and self.behavior_scores:
                probability_distribution = []
                for s in self.behavior_scores:
                    probability_distribution.append(float(s) / self.total_score)

                val = np.random.choice(self.behavior_names, p=probability_distribution,
                                       size=len(np.nonzero(probability_distribution)[0]), replace=False)
                return val
            else:
                return None
        else:
            raise ValueError('Unknown choice type: {}'.format(self.choice_type))


class Objective:
    __slots__ = [
        "objective",
        "behavior_id",
        "ignore_if_locked",
        "probability_to_require_objective",
        "random_completions_needed_min",
        "random_completions_needed_max",
    ]

    def __init__(self,
                 objective: str,
                 behavior_id: str,
                 ignore_if_locked: str,
                 probability_to_require_objective: float,
                 random_completions_needed_min: Optional[int] = 0,
                 random_completions_needed_max: Optional[int] = 0) -> None:
        self.objective = str(objective)
        self.behavior_id = str(behavior_id)
        self.ignore_if_locked = str(ignore_if_locked)
        self.probability_to_require_objective = float(probability_to_require_objective)
        self.random_completions_needed_min = \
            int(random_completions_needed_min) if random_completions_needed_min is not None else 0
        self.random_completions_needed_max = \
            int(random_completions_needed_min) if random_completions_needed_max is not None else 0

    @classmethod
    def from_json(cls, data: Dict):
        return cls(objective=data['objective'],
                   behavior_id=data['behaviorID'],
                   ignore_if_locked=data['ignoreIfLocked'],
                   probability_to_require_objective=data['probabilityToRequireObjective'],
                   random_completions_needed_min=data.get('randomCompletionsNeededMin', 0),
                   random_completions_needed_max=data.get('randomCompletionsNeededMax', 0))


class Activity:
    """ Activity representation class. """

    __slots__ = [
        "id",
        "type",
        "strategy",
    ]

    def __init__(self,
                 activity_id: str,
                 activity_type: str,
                 strategy: str) -> None:

        self.id = str(activity_id)
        self.type = str(activity_type)
        self.strategy = str(strategy)

    def choose(self):
        # TODO: method to choose from list of options
        # Some notes for this:
        # The Behavior chooser will provide a list of behaviors to try one at the time.
        # Since some behaviors will not always be available (like DriveOffCharger or ReactToObstacle), a method is
        # required to check wether a behavior can be run or not, and then execute it.
        # Once a behavior is executed, the behavior chooser needs to be notified of the action using
        # apply_repetition_penalty()
        # Until we have a better defined structure of the brain, this cannot be finished.
        pass


class BehaviorsActivity(Activity):
    __slots__ = [
        "behavior_chooser"
    ]

    def __init__(self,
                 behavior_chooser: BehaviorChooser,
                 *args, **kwargs):
        self.behavior_chooser = behavior_chooser
        super().__init__(*args, **kwargs)

    @classmethod
    def from_json(cls, data: Dict):
        return cls(
            BehaviorChooser.from_json(data['behaviorChooser'])
            if 'behaviorChooser' in data else None,
            activity_id=data['activityID'],
            activity_type=data['activityType'],
            strategy=data['activityStrategy']['type'])


class VoiceCommandActivity(Activity):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @classmethod
    def from_json(cls, data: Dict):
        return cls(
            activity_id=data['activityID'],
            activity_type=data['activityType'],
            strategy=data['activityStrategy']['type'])


class FeedingActivity(Activity):
    __slots__ = [
        "universal_chooser",
    ]

    def __init__(self,
                 universal_chooser: List[str],
                 *args, **kwargs) -> None:
        self.universal_chooser = universal_chooser
        super().__init__(*args, **kwargs)

    @classmethod
    def from_json(cls, data: Dict):
        return cls(
            universal_chooser=data['universalChooser']['behaviors']
            if 'universalChooser' in data else None,
            activity_id=data['activityID'],
            activity_type=data['activityType'],
            strategy=data['activityStrategy']['type'])


class FreeplayActivity(Activity):
    __slots__ = [
        "cube_only_activity",
        "face_only_activity",
        "face_and_cube_activity",
        "no_face_no_cube_activity",
        "sub_activities",
    ]

    def __init__(self,
                 cube_only_activity: str,
                 face_only_activity: str,
                 face_and_cube_activity: str,
                 no_face_no_cube_activity: str,
                 sub_activities: List,
                 *args, **kwargs) -> None:
        self.cube_only_activity = str(cube_only_activity)
        self.face_only_activity = str(face_only_activity)
        self.face_and_cube_activity = str(face_and_cube_activity)
        self.no_face_no_cube_activity = str(no_face_no_cube_activity)
        self.sub_activities = sub_activities

        super().__init__(*args, **kwargs)

    @classmethod
    def from_json(cls, data: Dict):
        return cls(
            cube_only_activity=data['desiredActivityNames']['cubeOnlyActivityName'],
            face_only_activity=data['desiredActivityNames']['faceOnlyActivityName'],
            face_and_cube_activity=data['desiredActivityNames']['faceAndCubeActivityName'],
            no_face_no_cube_activity=data['desiredActivityNames']['noFaceNoCubeActivityName'],
            sub_activities=data.get('subActivities'),
            activity_id=data['activityID'],
            activity_type=data['activityType'],
            strategy=data['activityStrategy']['type'])


class SparkedActivity(Activity):
    __slots__ = [
        "require_spark",
        "min_time",
        "max_time",
        "reps",
        "behavior_objective",
        "soft_spark_trigger",
        "behavior_chooser",
        "sub_activity_delegate",
        "spark_success_trigger",
        "spark_fail_trigger",
        "drive_start_trigger",
        "drive_loop_trigger",
        "drive_stop_trigger",
    ]

    def __init__(self,
                 require_spark: str,
                 min_time_secs: float,
                 max_time_secs: float,
                 reps: int,
                 behavior_objective: str,
                 soft_spark_trigger: str,
                 behavior_chooser: Optional[BehaviorChooser] = None,
                 sub_activity_delegate: Optional[Activity] = None,
                 spark_success_trigger: Optional[str] = None,
                 spark_fail_trigger: Optional[str] = None,
                 drive_start_trigger: Optional[str] = None,
                 drive_loop_trigger: Optional[str] = None,
                 drive_stop_trigger: Optional[str] = None,
                 *args, **kwargs) -> None:
        self.require_spark = str(require_spark)
        self.min_time = float(min_time_secs)
        self.max_time = float(max_time_secs)
        self.reps = int(reps)
        self.behavior_objective = str(behavior_objective)
        self.soft_spark_trigger = str(soft_spark_trigger)

        self.behavior_chooser = behavior_chooser
        self.sub_activity_delegate = sub_activity_delegate
        self.spark_success_trigger = spark_success_trigger
        self.spark_fail_trigger = spark_fail_trigger

        self.drive_start_trigger = drive_start_trigger
        self.drive_loop_trigger = drive_loop_trigger
        self.drive_stop_trigger = drive_stop_trigger

        super().__init__(*args, **kwargs)

    @classmethod
    def from_json(cls, data: Dict):
        if 'subActivityDelegate' in data:
            sub_act_delegate = from_dict(data['subActivityDelegate'])
        else:
            sub_act_delegate = None
        return cls(
            require_spark=data['requireSpark'],
            min_time_secs=data['minTimeSecs'],
            max_time_secs=data['maxTimeSecs'],
            reps=data['numberOfRepetitions'],
            behavior_objective=data['behaviorObjective'],
            soft_spark_trigger=data['softSparkTrigger'],
            behavior_chooser=BehaviorChooser.from_json(data['behaviorChooser'])
            if 'behaviorChooser' in data else None,
            sub_activity_delegate=sub_act_delegate,
            spark_success_trigger=data.get('sparksSuccessTrigger'),
            spark_fail_trigger=data.get('sparksFailTrigger'),
            drive_start_trigger=data.get('driveStartAnimTrigger'),
            drive_loop_trigger=data.get('driveLoopAnimTrigger'),
            drive_stop_trigger=data.get('driveStopAnimTrigger'),
            activity_id=data['activityID'],
            activity_type=data['activityType'],
            strategy=data['activityStrategy']['type'])


class PyramidActivity(Activity):
    __slots__ = [
        "setup_chooser",
        "build_chooser",
        "interlude_chooser",
        "needs_action_id",
    ]

    def __init__(self,
                 setup_chooser: BehaviorChooser,
                 build_chooser: BehaviorChooser,
                 interlude_chooser: Optional[BehaviorChooser] = None,
                 needs_action_id: Optional[str] = None,
                 *args, **kwargs):
        self.setup_chooser = setup_chooser
        self.build_chooser = build_chooser
        self.interlude_chooser = interlude_chooser
        self.needs_action_id = needs_action_id

        super().__init__(*args, **kwargs)

    @classmethod
    def from_json(cls, data: Dict):
        return cls(
            setup_chooser=BehaviorChooser.from_json(data['setupChooser']),
            build_chooser=BehaviorChooser.from_json(data['buildChooser']),
            interlude_chooser=BehaviorChooser.from_json(data['interludeBehaviorChooser'])
            if 'interludeBehaviorChooser' in data else None,
            needs_action_id=data.get('needsActionID'),
            activity_id=data['activityID'],
            activity_type=data['activityType'],
            strategy=data['activityStrategy']['type'])


class SocializeActivity(Activity):
    __slots__ = [
        "behavior_chooser",
        "interlude_chooser",
        "max_face_iterations",
        "required_objectives",
    ]

    def __init__(self,
                 behavior_chooser: BehaviorChooser,
                 interlude_chooser: BehaviorChooser,
                 max_face_iterations: int,
                 required_objectives: List[Objective],
                 *args, **kwargs):
        self.behavior_chooser = behavior_chooser
        self.interlude_chooser = interlude_chooser
        self.max_face_iterations = int(max_face_iterations)
        self.required_objectives = required_objectives

        super().__init__(*args, **kwargs)

    @classmethod
    def from_json(cls, data: Dict):
        return cls(
            behavior_chooser=BehaviorChooser.from_json(data['behaviorChooser']),
            interlude_chooser=BehaviorChooser.from_json(data['interludeBehaviorChooser']),
            max_face_iterations=data['maxNumFindFacesSearchIterations'],
            required_objectives=[Objective.from_json(d) for d in data['requiredObjectives']],
            activity_id=data['activityID'],
            activity_type=data['activityType'],
            strategy=data['activityStrategy']['type'])


class NeedsActivity(Activity):
    __slots__ = [
        "behavior_chooser"
    ]

    def __init__(self,
                 behavior_chooser: BehaviorChooser,
                 *args, **kwargs):
        self.behavior_chooser = behavior_chooser
        super().__init__(*args, **kwargs)

    @classmethod
    def from_json(cls, data: Dict):
        return cls(
            behavior_chooser=BehaviorChooser.from_json(data['behaviorChooser']),
            activity_id=data['activityID'],
            activity_type=data['activityType'],
            strategy=data['activityStrategy']['type'])


def from_dict(info: Dict) -> Activity:
    if info['activityType'] == 'VoiceCommand':
        return VoiceCommandActivity.from_json(info)

    elif info['activityType'] == 'BehaviorsOnly':
        return BehaviorsActivity.from_json(info)

    elif info['activityType'] == 'Feeding':
        return FeedingActivity.from_json(info)

    elif info['activityType'] == 'Freeplay':
        return FreeplayActivity.from_json(info)

    elif info['activityType'] == 'Sparked':
        return SparkedActivity.from_json(info)

    elif info['activityType'] == 'BuildPyramid':
        return PyramidActivity.from_json(info)

    elif info['activityType'] == 'Socialize':
        return SocializeActivity.from_json(info)

    elif info['activityType'] == 'NeedsExpression':
        return NeedsActivity.from_json(info)

    else:
        return Activity(
            activity_id=info['activityID'],
            activity_type=info['activityType'],
            strategy=info['activityStrategy']['type']
        )


def load_activities(resource_dir: str) -> Dict[str, Activity]:
    """ Load activity map from cozmo resources. """

    # TODO: cozmo_resources/config/engine/needs_action_config.json
    # TODO: cozmo_resources/config/engine/do_a_trick_weights.json

    start_time = time.perf_counter()

    activity_folders = [
        os.path.join('cozmo_resources', 'config', 'engine', 'behaviorSystem', 'activities_config.json'),
        os.path.join('cozmo_resources', 'config', 'engine', 'behaviorSystem', 'behavior_system_config.json'),
        os.path.join('cozmo_resources', 'config', 'engine', 'behaviorSystem', 'activities')
    ]
    activity_files = get_json_files(resource_dir, activity_folders)

    activities = {}

    for filename in activity_files:
        json_data = load_json_file(filename)
        if isinstance(json_data, list):
            for activity in json_data:
                activities[activity['activityID']] = from_dict(activity)
        else:
            activities[json_data['activityID']] = from_dict(json_data)

    logger.debug("Loaded {} activities in {:.02f} s.".format(len(activities), time.perf_counter() - start_time))

    return activities
