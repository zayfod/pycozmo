"""

Activity classes.

"""

import json
import os
from typing import Dict, List, Optional


__all__ = [
    "Activity",

    "load_activities",
]


class BehaviorChooser:

    def __init__(self,
                 choice_type: str,
                 behaviors: List) -> None:

        self.choice_type = choice_type
        self.behaviors = behaviors
        self.iteration = 0

    @classmethod
    def from_json(cls, data: Dict):
        return cls(
            choice_type=data['type'],
            behaviors=data['behaviors'] if 'behaviors' in data else []
        )

    def reset(self):
        self.iteration = 0

    def choose(self):
        if self.choice_type == 'Selection':
            return None
        if self.choice_type == 'StrictPriority':
            if self.iteration <= len(self.behaviors):
                out = self.behaviors[self.iteration]
                self.iteration += 1
                return out
            else:
                return None
        elif self.choice_type == 'Scoring':
            #TODO: add score based choice method
            pass
        else:
            print(self.choice_type)
        return None


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
        pass


class BehaviorsActivity(Activity):
    def __init__(self,
                 behavior_chooser: BehaviorChooser,
                 *args, **kwargs):
        self.behavior_chooser = behavior_chooser
        super().__init__(*args, **kwargs)

    def choose(self):
        if self.behavior_chooser:
            return self.behavior_chooser.choose()


class VoiceCommandActivity(Activity):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class FeedingActivity(Activity):
    def __init__(self,
                 universal_chooser: List[str],
                 *args, **kwargs) -> None:
        self.universal_chooser = universal_chooser
        super().__init__(*args, **kwargs)

    def choose(self):
        if self.universal_chooser:
            return self.universal_chooser


class FreeplayActivity(Activity):
    def __init__(self,
                 cube_only_activity: str,
                 face_only_activity: str,
                 face_and_cube_activity: str,
                 no_face_no_cube_activity: str,
                 sub_activities: List,
                 *args, **kwargs) -> None:
        self.cube_only_activity = cube_only_activity
        self.face_only_activity = face_only_activity
        self.face_and_cube_activity = face_and_cube_activity
        self.no_face_only_activity = no_face_no_cube_activity
        self.sub_activities = sub_activities

        super().__init__(*args, **kwargs)


class SparkedActivity(Activity):
    def __init__(self,
                 require_spark: str,
                 min_time_secs: float,
                 max_time_secs: float,
                 reps: int,
                 behavior_objective: str,
                 soft_spark_trigger: str,
                 behavior_chooser: Optional[BehaviorChooser] = None,
                 #TODO: class for activity_delegate
                 sub_activity_delegate: Optional[Dict] = None,
                 spark_success_trigger: Optional[str] = None,
                 spark_fail_trigger: Optional[str] = None,
                 drive_start_trigger: Optional[str] = None,
                 drive_loop_trigger: Optional[str] = None,
                 drive_stop_trigger: Optional[str]=None,
                 *args, **kwargs) -> None:
        self.require_spark = require_spark
        self.min_time = min_time_secs
        self.max_time = max_time_secs
        self.reps = reps
        self.behavior_objective = behavior_objective
        self.soft_spark_trigger =soft_spark_trigger

        self.behavior_chooser = behavior_chooser
        self.sub_activity_delegate = sub_activity_delegate
        self.spark_success_trigger = spark_success_trigger
        self.spark_fail_trigger = spark_fail_trigger

        self.drive_start_trigger = drive_start_trigger
        self.drive_loop_trigger = drive_loop_trigger
        self.drive_stop_trigger = drive_stop_trigger

        super().__init__(*args, **kwargs)

    def choose(self):
        if self.behavior_chooser:
            return self.behavior_chooser.choose()


class PyramidActivity(Activity):
    def __init__(self,
                 setup_chooser: BehaviorChooser,
                 build_chooser: BehaviorChooser,
                 interlude_chooser: BehaviorChooser,
                 *args, **kwargs):
        self.setup_chooser = setup_chooser
        self.build_chooser = build_chooser
        self.interlude_chooser = interlude_chooser

        super().__init__(*args, **kwargs)

    def choose(self):
        if self.setup_chooser:
            return self.setup_chooser.choose()


class SocializeActivity(Activity):
    def __init__(self,
                 behavior_chooser: BehaviorChooser,
                 interlude_chooser: BehaviorChooser,
                 max_face_iterations: int,
                 #TODO: class for objectives
                 required_objectives: List,
                *args, **kwargs):
        self.behavior_chooser = behavior_chooser
        self.interlude_chooser = interlude_chooser
        self.max_face_iterations = max_face_iterations
        self.required_objectives = required_objectives

        super().__init__(*args, **kwargs)

    def choose(self):
        if self.behavior_chooser:
            return self.behavior_chooser.choose()


class NeedsActivity(Activity):
    def __init__(self,
                 behavior_chooser: BehaviorChooser,
                 *args, **kwargs):
        self.behavior_chooser = behavior_chooser
        super().__init__(*args, **kwargs)

    def choose(self):
        if self.behavior_chooser:
            return self.behavior_chooser.choose()


def from_dict(info: Dict) -> Activity:
    if info['activityType'] == 'VoiceCommand':
        return VoiceCommandActivity(
            activity_id=info['activityID'],
            activity_type=info['activityType'],
            strategy=info['activityStrategy']['type'])

    elif info['activityType'] == 'BehaviorsOnly':
        return BehaviorsActivity(
            BehaviorChooser.from_json(info['behaviorChooser'])
                if 'behaviorChooser' in info else None,
            activity_id=info['activityID'],
            activity_type=info['activityType'],
            strategy=info['activityStrategy']['type'])

    elif info['activityType'] == 'Feeding':
        return FeedingActivity(
            universal_chooser=info['universalChooser']['behaviors']
                                if 'universalChooser' in info else None,
            activity_id=info['activityID'],
            activity_type=info['activityType'],
            strategy=info['activityStrategy']['type'])

    elif info['activityType'] == 'Freeplay':
        return FreeplayActivity(
            cube_only_activity=info['desiredActivityNames']['cubeOnlyActivityName'],
            face_only_activity=info['desiredActivityNames']['faceOnlyActivityName'],
            face_and_cube_activity=info['desiredActivityNames']['faceAndCubeActivityName'],
            no_face_no_cube_activity=info['desiredActivityNames']['noFaceNoCubeActivityName'],
            sub_activities=info['subActivities'] if 'subActivities' in info else None,
            activity_id=info['activityID'],
            activity_type=info['activityType'],
            strategy=info['activityStrategy']['type'])

    elif info['activityType'] == 'Sparked':
        return SparkedActivity(
            require_spark=info['requireSpark'],
            min_time_secs=info['minTimeSecs'],
            max_time_secs=info['maxTimeSecs'],
            reps=info['numberOfRepetitions'],
            behavior_objective=info['behaviorObjective'],
            soft_spark_trigger=info['softSparkTrigger'],
            behavior_chooser=BehaviorChooser.from_json(info['behaviorChooser'])
                if 'behaviorChooser' in info else None,
            sub_activity_delegate=info['subActivityDelegate'] if 'subActivityDelegate' in info else None,
            spark_success_trigger=info['sparksSuccessTrigger'] if 'sparksSuccessTrigger' in info else None,
            spark_fail_trigger=info['sparksFailTrigger'] if 'sparksFailTrigger' in info else None,
            drive_start_trigger=info['driveStartAnimTrigger'] if 'driveStartAnimTrigger' in info else None,
            drive_loop_trigger=info['driveLoopAnimTrigger'] if 'driveLoopAnimTrigger' in info else None,
            drive_stop_trigger=info['driveStopAnimTrigger'] if 'driveStopAnimTrigger' in info else None,
            activity_id=info['activityID'],
            activity_type=info['activityType'],
            strategy=info['activityStrategy']['type'])

    elif info['activityType'] == 'BuildPyramid':
        return PyramidActivity(
            setup_chooser=BehaviorChooser.from_json(info['setupChooser']),
            build_chooser=BehaviorChooser.from_json(info['buildChooser']),
            interlude_chooser=BehaviorChooser.from_json(info['interludeBehaviorChooser']),
            activity_id=info['activityID'],
            activity_type=info['activityType'],
            strategy=info['activityStrategy']['type'])

    elif info['activityType'] == 'Socialize':
        return SocializeActivity(
            behavior_chooser=BehaviorChooser.from_json(info['behaviorChooser']),
            interlude_chooser=BehaviorChooser.from_json(info['interludeBehaviorChooser']),
            max_face_iterations=info['maxNumFindFacesSearchIterations'],
            required_objectives=info['requiredObjectives'],
            activity_id=info['activityID'],
            activity_type=info['activityType'],
            strategy=info['activityStrategy']['type'])

    elif info['activityType'] == 'NeedsExpression':
        return NeedsActivity(
            behavior_chooser=BehaviorChooser.from_json(info['behaviorChooser']),
            activity_id=info['activityID'],
            activity_type=info['activityType'],
            strategy=info['activityStrategy']['type'])

    else:
        return Activity(
            activity_id=info['activityID'],
            activity_type=info['activityType'],
            strategy=info['activityStrategy']['type']
        )


def get_activity_files(resource_dir: str) -> List[str]:
    activity_files = [resource_dir + '/cozmo_resources/config/engine/behaviorSystem/activities_config.json']
    activity_folder = resource_dir + '/cozmo_resources/config/engine/behaviorSystem/activities/'
    for root, dirs, files in os.walk(activity_folder):
        for name in files:
            if name.endswith((".json")):
                activity_files.append(os.path.join(root, name))
    return activity_files


def load_activities(resource_dir: str) -> Dict[str, Activity]:
    activities = {}
    activity_files = get_activity_files(resource_dir)

    for filename in activity_files:
        with open(filename, 'r') as cf:
            filtered_json = ''
            for line in cf.readlines():
                if '//' in line:
                    wordlist = line.split(' ')
                    # get all words before '//'
                    line = ' '.join(wordlist[:wordlist.index('//')])
                filtered_json += line
            json_data = json.loads(filtered_json)
            if isinstance(json_data, list):
                for activity in json_data:
                    activities[activity['activityID']] = from_dict(activity)
            else:
                activities[json_data['activityID']] = from_dict(json_data)

    return activities


