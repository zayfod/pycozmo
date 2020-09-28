"""

Activity classes.

"""

from typing import Dict


__all__ = [
    "Activity",

    "load_activities",
]


class Activity:
    """ Activity representation class. """

    __slots__ = [
        "id",
        "type",
        "behavior_chooser",
        "strategy",
    ]

    def __init__(self,
                 activity_id: str,
                 activity_type: str,
                 behavior_chooser: str,
                 strategy: str) -> None:
        self.id = str(activity_id)
        self.type = str(activity_type)
        self.behavior_chooser = str(behavior_chooser)
        self.strategy = str(strategy)


def load_activities() -> Dict[str, Activity]:
    # TODO: Load:
    #  - cozmo_resources/config/engine/behaviorSystem/activities_config.json
    #  - cozmo_resources/config/engine/behaviorSystem/activities/*/*.json
    activities = {}
    return activities
